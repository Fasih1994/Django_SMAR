from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import (
    Organization,
    Topics, 
    Package, 
    UserRole, 
    User)
from django.db import IntegrityError
from datetime import datetime
from decimal import Decimal


def create_user(email, password, organization=None, package=1, role=1):
    if not organization:
        raise ValueError("user must have an organization.")
    user = get_user_model().objects.create_user(email=email, password=password)
    user.organization=organization
    user.package=package
    user.role=role
    
    user.save()
    return user


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        package = Package.objects.create(
            name = 'pro',
            price = Decimal('200.00')
        )
        organization = Organization.objects.create(
            name = 'inseyab'
        )
        userrole = UserRole.objects.create(
            name = 'adminone'
        )
        """Creating a user with an email is successful"""        
        user = get_user_model().objects.create_user(
            email='test@example.com', password="testpass123", package=package,
            organization=organization,
            role=userrole
            )

        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password("testpass123"))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            package = Package.objects.create(
                name = 'pro',
                price = Decimal('200.00')
            )
            organization = Organization.objects.create(
                name = 'inseyab'
            )
            userrole = UserRole.objects.create(
                name = 'adminone'
            )
            user = get_user_model().objects.create_user(
                email = email,
                password = 'sample123',
                organization = organization,
                package = package,
                role = userrole
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        package = Package.objects.create(
            name = 'pro',
            price = Decimal('200.00')
        )
        organization = Organization.objects.create(
            name = 'inseyab'
        )
        userrole = UserRole.objects.create(
            name = 'adminone'
        )    
        """User without email raises error on creation"""
        with self.assertRaises(ValueError):
            _ = get_user_model().objects.create_user(
                '', "pas123",
                organization = organization,
                package = package,
                role = userrole
            )

    def test_create_superuser(self):
        package = Package.objects.create(
            name='pro',
            price=Decimal('200.00')
        )
        organization = Organization.objects.create(
            name='inseyab'
        )
        userrole = UserRole.objects.create(
            name='adminone'
        )
        """Test Creating a superuser"""
        SUPERUSER_EMAIL = 'test@example.com'
        SUPERUSER_PASSWORD = 'tset123'
        user = get_user_model().objects.create_superuser(
            SUPERUSER_EMAIL, SUPERUSER_PASSWORD,
            organization=organization,
            package=package,
            role=userrole
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_check_org_model(self):
        """test creating an organization"""
        
        organization = Organization.objects.create(
            name='inseyab',
            description='django Rest_framework',
            linkedin_profile='https://ca.linkedin.com/in/abrar',
            industry='computer_science',
            created_by=125,
            last_updated_by=125,
            last_update_login=125
        )
        org = Organization.objects.get(name='inseyab')
        self.assertIsNotNone(organization.creation_date)
        self.assertIsNotNone(organization.last_update_date)
        self.assertEqual(organization.name, 'inseyab')
        self.assertEqual(organization.description, 'django Rest_framework')
        self.assertEqual(organization.linkedin_profile,
                         'https://ca.linkedin.com/in/abrar')
        self.assertEqual(organization.industry, 'computer_science')
        
    def test_package_model(self):
        package = Package.objects.create(
            name = 'pro',
            price = Decimal('200.00'),
            created_by = 1,
            last_updated_by = 102,
            last_update_login = 102
        )    
        package = Package.objects.get(
            name = 'pro'
        )
        self.assertIsNotNone(package.creation_date)
        self.assertIsNotNone(package.last_update_date)
        self.assertEqual(package.name, 'pro')
        self.assertEqual(package.price, Decimal('200.00'))
        self.assertEqual(package.created_by, 1)
        self.assertEqual(package.last_updated_by, 102)
        self.assertEqual(package.last_update_login, 102)
        
    def test_check_userRole_model(self):
        userrole = UserRole.objects.create(
            name = 'adminone',
            created_by = 1,
            last_updated_by = 106,
            last_update_login = 106
        )
        role = UserRole.objects.get(
            name = 'adminone'
        )
        self.assertEqual(userrole.name, 'adminone')
        self.assertIsNotNone(userrole.creation_date)
        self.assertIsNotNone(userrole.last_update_date)
        self.assertEqual(userrole.created_by, 1)
        self.assertEqual(userrole.last_updated_by, 106)
        self.assertEqual(userrole.last_update_login, 106)

    def test_check_topics_model(self):
        organization = Organization.objects.create(
            name = 'inseyab'
        )
        package = Package.objects.create(
            name = 'basic'
        )
        role = UserRole.objects.create(
            name = 'admin'
        )
        user=User.objects.create(
            name = 'testuser',
            email = 'test@email.com',
            password = 'testpass',
            organization = organization,
            package = package,
            role = role
        )
        topic = Topics.objects.create(
            name = 'physics',
            platform = 'airforce',
            keywords = 'nastp',
            prompt = 'xyz',
            status = 'A',
            created_by = 1,
            last_updated_by = 105,
            last_update_login = 105,
            user = user
        )
        topic = Topics.objects.get(
            name = 'physics'
        )
        self.assertEqual(topic.name, 'physics')
        self.assertEqual(topic.platform, 'airforce')
        self.assertEqual(topic.keywords, 'nastp')
        self.assertEqual(topic.prompt, 'xyz')
        self.assertEqual(topic.status, 'A')
        self.assertEqual(topic.created_by, 1)
        self.assertEqual(topic.last_updated_by, 105)
        self.assertEqual(topic.last_update_login, 105)
        self.assertIsNotNone(topic.last_update_date)
        self.assertIsNotNone(topic.creation_date)