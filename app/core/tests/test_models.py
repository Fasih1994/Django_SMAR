from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import (
    Organization, 
    # PackageStatus, 
    Package, 
    UserRole, 
    User)
from django.db import IntegrityError
from datetime import datetime


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        package = Package.objects.create(
            package_name = 'pro',
            package_price = 200
        )
        organization = Organization.objects.create(
            organization_name = 'inseyab'
        )
        userrole = UserRole.objects.create(
            user_role_name = 'tradeforesight'
        )
        """Creating a user with an email is successful"""

        email = 'test@example.com'
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password, package_id=package.id,
            organization_id=organization.id,
            user_role_id=userrole.id,
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
            package = Package.objects.create(
                package_name = 'pro',
                package_price = 'inseyab'
            )
            organization = Organization.objects.create(
                organization_name = 'inseyab'
            )
            userrole = UserRole.objects.create(
                user_role_name = 'tradeforesight'
            )
            user = get_user_model().objects.create_user(
                email, 'sample123',
                organization_id = organization,
                package_id = package,
                user_role_id = userrole
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        package = Package.objects.create(
            package_name = 'pro',
            package_price = 200
        )
        organization = organization.objects.create(
            organization_name = 'inseyab'
        )
        userrole = UserRole.objects.create(
            user_role_name = 'tradeforsight'
        )    
        """User without email raises error on creation"""
        with self.assertRaises(ValueError):
            _ = get_user_model().objects.create_user(
                '', "pas123",
                organization_id = organization,
                package_id = package,
                user_role_id = userrole
            )

    def test_create_superuser(self):
        package = Package.objects.create(
            package_name='pro',
            package_price=200
        )
        organization = Organization.objects.create(
            organization_name='inseyab'
        )
        userrole = UserRole.objects.create(
            user_role_name='tradeforesight'
        )
        """Test Creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'tset123',
            organization_id=organization,
            package_id=package,
            user_role_id=userrole
            )
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
    
    # def tests_check_package_status(self):
    #     organization = Organization.objects.create(
    #         organization_name='inseyab'
    #     )
    #     package = Package.objects.create(
    #         package_name = 'pro',
    #         package_price = 200
    #     )
    #     package_status = PackageStatus.objects.create(
    #         organization_id = organization,
    #         package_id = package,
    #         package_status = 'valid',
    #         package_start_date = '2023-03-13',
    #         package_end_date = '2024-03-13',
    #         created_by = 1,
    #         last_updated_by = 101,
    #         last_update_login = 1
    #     )    
    #     package_status = PackageStatus.objects.get(
    #         package_id = package_status.package_id
    #     )
    #     self.assertEqual(package_status.package_status, 'valid')
    #     self.assertEqual(str(package_status.package_start_date), '2023-03-13')
    #     self.assertEqual(str(package_status.package_end_date), '2024-03-13')
    #     self.assertEqual(package_status.created_by, 1)
    #     self.assertEqual(package_status.last_updated_by, 101)
    #     self.assertEqual(package_status.last_update_login, 1)
    #     self.assertIsNotNone(package_status.creation_date)
    #     self.assertIsNotNone(package_status.last_update_date)
    #     self.assertLess(
    #         package_status.package_start_date,
    #         package_status.package_end_date
    #     )
    #     self.assertGreater(
    #         package_status.package_end_date,
    #         package_status.package_start_date
    #     )
        
    def test_package_model(self):
        package = Package.objects.create(
            name = 'pro',
            price = 200,
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
        self.assertEqual(package.price, 200)
        self.assertEqual(package.created_by, 1)
        self.assertEqual(package.last_updated_by, 102)
        self.assertEqual(package.last_update_login, 102)
        
    def tests_check_userRole_model(self):
        userrole = UserRole.objects.create(
            user_role_name = 'tradeforsight',
            created_by = 1,
            last_updated_by = 106,
            last_update_login = 106
        )
        userrole = UserRole.objects.get(
            user_role_id = userrole.user_role_id
        )
        self.assertEqual(userrole.user_role_name, 'tradeforsight')
        self.assertIsNotNone(userrole.creation_date)
        self.assertIsNotNone(userrole.last_update_date)
        self.assertEqual(userrole.created_by, 1)
        self.assertEqual(userrole.last_updated_by, 106)
        self.assertEqual(userrole.last_update_login, 106)
