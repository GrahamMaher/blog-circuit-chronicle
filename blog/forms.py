from django import forms
from .models import Comment, NewsletterSubscription

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

# Newsletter subscription form
class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']