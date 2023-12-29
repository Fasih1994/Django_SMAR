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

    # def tests_create_new_organization_with_orgname_and_orgid_successfull(self):
    #     org_id = 101
    #     org_name = "inseyab"
    #     organization = Organization.objects.create(
    #         organization_id=org_id, organization_name="inseyab")
    #     self.assertEqual(Organization.objects.all().count(), 1)
    #     self.assertEqual(organization.organization_id, org_id)
    #     self.assertEqual(organization.organization_name, org_name)

    # def tests_organization_id_dealing_with_pk(self):
    #     org_id = 101
    #     Organization.objects.create(organization_id=org_id)
    #     with self.assertRaises(IntegrityError) as same_id:
    #         """create second org id with the same id"""
    #         Organization.objects.create(organization_id=org_id)
    #     self.assertIn(str(org_id), str(same_id.exception))

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
