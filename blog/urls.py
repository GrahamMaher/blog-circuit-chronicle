from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),  # List all posts
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),  # Post details
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category_detail'),  # Category view
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag_detail'),  # Tag view
    path('comment/<int:post_id>/', views.comment_create, name='create_comment'),  # Create comment
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),  # Newsletter signup
]