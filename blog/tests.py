# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from .forms import CommentForm

class BlogViewsTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            status=1
        )
        
        # Create a comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a test comment.'
        )

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'This is a test post.')  # Check if the post content is in the response

    def test_comment_edit_view(self):
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.post(reverse('comment_edit', args=[self.post.slug, self.comment.id]), {
            'body': 'This is an updated comment.'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.comment.refresh_from_db()  # Refresh the comment instance
        self.assertEqual(self.comment.body, 'This is an updated comment.')  # Check if the comment was updated

    def test_comment_delete_view(self):
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.post(reverse('comment_delete', args=[self.post.slug, self.comment.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())  # Check if the comment was deleted

    def test_like_post_view(self):
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())  # Check if like was created

        # Test unliking the post
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())  # Check if like was removed

    def test_like_post_view_not_authenticated(self):
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)  # Check if the login required page is rendered
        self.assertTemplateUsed(response, 'blog/login_required.html')  # Check if the correct template is used
