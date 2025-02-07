from django.test import TestCase
from .models import About, CollaborateRequest

class AboutModelTest(TestCase):
    def setUp(self):
        self.about = About.objects.create(
            title='About Me',
            profile_image='path/to/image.jpg',  # Use a valid Cloudinary image path or mock it
            content='This is a test about me.'
        )

    def test_about_creation(self):
        self.assertEqual(self.about.title, 'About Me')
        self.assertEqual(self.about.content, 'This is a test about me.')
        self.assertIsNotNone(self.about.updated_on)  # Check if updated_on is set

    def test_string_representation(self):
        self.assertEqual(str(self.about), 'About Me')


class CollaborateRequestModelTest(TestCase):
    def setUp(self):
        self.request = CollaborateRequest.objects.create(
            name='John Doe',
            email='john.doe@example.com',
            message='I would like to collaborate with you.',
            read=False
        )

    def test_collaborate_request_creation(self):
        self.assertEqual(self.request.name, 'John Doe')
        self.assertEqual(self.request.email, 'john.doe@example.com')
        self.assertEqual(self.request.message, 'I would like to collaborate with you.')
        self.assertFalse(self.request.read)  # Check if read is False

    def test_string_representation(self):
        self.assertEqual(str(self.request), 'Collaboration request from John Doe')