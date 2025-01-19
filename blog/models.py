from django.db import models
from django.contrib.auth.models import User

# Post Status Options
STATUS = ((0, "Draft"), (1, "Published"))

class UserProfile(models.Model):
    """Extend the default User model to include additional profile details."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True)  # For storing social media links

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Category(models.Model):
    """Categories for organizing blog posts."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tags for organizing blog posts."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Model for blog posts."""
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to="featured_images/", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    """Model for comments on blog posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class NewsletterSubscription(models.Model):
    """Model for managing newsletter subscriptions."""
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Newsletter subscription: {self.email}"


class ContactMessage(models.Model):
    """Model for handling contact form submissions."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"