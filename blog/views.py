from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Blog, Blogger, Comment
from .forms import UserRegistrationForm, BlogForm, CommentForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.utils.text import slugify
import re

def index(request):
    """View function for home page of site."""
    num_blogs = Blog.objects.all().count()
    num_bloggers = Blogger.objects.count()
    num_comments = Comment.objects.count()

    context = {
        'num_blogs': num_blogs,
        'num_bloggers': num_bloggers,
        'num_comments': num_comments,
    }

    return render(request, 'index.html', context=context)

def search_blogs(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(author__user__username__icontains=query)
        ).distinct()
    else:
        blogs = Blog.objects.all()
    return render(request, 'blog/search_results.html', {'blogs': blogs, 'query': query})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Blogger profile for the new user
            Blogger.objects.create(user=user)
            # Redirect to login page instead of auto-login
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class BlogListView(ListView):
    model = Blog
    paginate_by = 5
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_list'

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        
        # Get related blogs based on content similarity
        words = set(re.findall(r'\w+', blog.description.lower()))
        related_blogs = Blog.objects.exclude(id=blog.id)[:3]
        
        # Sort related blogs by similarity
        related_blogs = sorted(related_blogs, 
                             key=lambda x: len(set(re.findall(r'\w+', x.description.lower())) & words),
                             reverse=True)
        
        context['related_blogs'] = related_blogs
        return context

class BloggerListView(ListView):
    model = Blogger
    template_name = 'blog/blogger_list.html'
    context_object_name = 'blogger_list'

class BloggerDetailView(DetailView):
    model = Blogger
    template_name = 'blog/blogger_detail.html'
    context_object_name = 'blogger'

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['description']
    template_name = 'blog/comment_form.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super().form_valid(form)

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = Blogger.objects.get(user=self.request.user)
        return super().form_valid(form)
