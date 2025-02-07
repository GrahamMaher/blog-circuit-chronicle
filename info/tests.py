from django.test import TestCase
from .models import About, CollaborateRequest


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
        self.assertEqual(self.request.message, 'Request to work with you.')
        self.assertFalse(self.request.read)

    def test_string_representation(self):
        self.assertEqual(str(self.request), 'Request from John Doe')
