from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('blog/<int:pk>/create/', views.CommentCreate.as_view(), name='comment-create'),
    path('register/', views.register, name='register'),
    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('search/', views.search_blogs, name='search'),
] 