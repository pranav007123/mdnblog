from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, help_text="Enter your bio details here.")

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Blogger, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2000, help_text="Enter your blog text here.")
    post_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['post_date']

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.blog.id)])

    def __str__(self):
        len_title = 75
        if len(self.description) > len_title:
            return f"{self.description[:len_title]}..."
        return self.description
