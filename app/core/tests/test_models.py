# from unittest.mock import patch, Mock
# from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

# from core import models


def create_user(email='user@example.com',
                password='testpass123') -> get_user_model():
    """Create and return a new user"""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """Test models

    Args:
        TestCase (_type_): _description_
    """

    def test_create_user_with_email_successful(self):
        """Creating a user with an email is successful
        """

        email = 'test@example.com'
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """User without email raises error on creaton"""
        with self.assertRaises(ValueError):
            _ = get_user_model().objects.create_user('', "pas123")

    def test_create_superuser(self):
        """Test Creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'tset123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
