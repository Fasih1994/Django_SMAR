from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Organization
from django.db import IntegrityError


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Creating a user with an email is successful"""

        email = 'test@example.com'
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password)

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
        """User without email raises error on creation"""
        with self.assertRaises(ValueError):
            _ = get_user_model().objects.create_user('', "pas123")

    def test_create_superuser(self):
        """Test Creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'tset123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def tests_create_new_organization_with_orgname_and_orgid_successfull(self):
        org_id = 101
        org_name = "inseyab"
        organization = Organization.objects.create(
            organization_id=org_id, organization_name="inseyab")
        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(organization.organization_id, org_id)
        self.assertEqual(organization.organization_name, org_name)

    def tests_organization_id_dealing_with_pk(self):
        org_id = 101
        Organization.objects.create(organization_id=org_id)
        with self.assertRaises(IntegrityError) as same_id:
            """create second org id with the same id"""
            Organization.objects.create(organization_id=org_id)
        self.assertIn(str(org_id), str(same_id.exception))

    def test_check_org_model(self):
        """test creating an organization"""

        organization = Organization.objects.create(
            organization_name='inseyab',
            description='django Rest_framework',
            linkedin_profile='https://ca.linkedin.com/in/abrar',
            industry='computer_science',
            created_by=125,
            last_updated_by=125,
            last_update_login=125
        )
        organization = Organization.objects.get(organization_id=1)
        self.assertIsNotNone(organization.creation_date)
        self.assertIsNotNone(organization.last_update_date)
        self.assertEqual(organization.organization_name, 'inseyab')
        self.assertEqual(organization.description, 'django Rest_framework')
        self.assertEqual(organization.linkedin_profile,
                         'https://ca.linkedin.com/in/abrar')
        self.assertEqual(organization.industry, 'computer_science')
