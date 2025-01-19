from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag, Comment, NewsletterSubscription
from .forms import CommentForm, NewsletterSubscriptionForm

# View to list all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

# View to show a single post's details
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# View for Category-specific posts
class CategoryView(ListView):
    model = Post
    template_name = 'blog/category_detail.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Post.objects.filter(category=category)

# View for Tag-specific posts
class TagView(ListView):
    model = Post
    template_name = 'blog/tag_detail.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags=tag)

# Handle comment creation
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})

# Handle newsletter signup
def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newsletter_signup')
    else:
        form = NewsletterSubscriptionForm()
    return render(request, 'blog/newsletter_signup.html', {'form': form})

# About page view
def about(request):
    return render(request, 'blog/about.html')

# Contact page view
def contact(request):
    if request.method == 'POST':
        # Process contact form data (not implemented here)
        pass
    return render(request, 'blog/contact.html')