# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from .forms import CommentForm

class BlogViewsTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser',  
                                             password='testpass')
        
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            status=1
        )
        
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a test comment.'
        )

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail',
                                            args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'This is a test post.')

    def test_comment_edit_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('comment_edit', 
                                    args=[self.post.slug, self.comment.id]), {
            'body': 'This is an updated comment.'
        })
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, 'This is an updated comment.')
    def test_comment_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('comment_delete', 
                                            args=[self.post.slug, self.comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_like_post_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post)
                                            .exists())

        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_like_post_view_not_authenticated(self):
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/login_required.html')
