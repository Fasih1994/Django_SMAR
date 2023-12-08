# from unittest.mock import patch, Mock
# from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Organization, get_organization_model, Package

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

    def test_check_org_model(self):
        """test creating an organization"""            
        organization=Organization.objects.create(
        organization_id=101,
        organization_name= 'my_org',
        package_id=1,
        package_status=1,
        package_start_date='01/01/2020',
        package_end_date='01/01/2024',
        creation_date='01/01/2018',
        created_by='oneuser',
        last_update_date='01/01/2022',
        last_updated_by='123',
        last_update_login='123',
        )   
        organization=Organization.objects.get(id=organization.id)
        organization_id = f'{organization.organization_id}'
        organization_name =f'{organization.organization_name}'
        package_id = f'{organization.package_id}'
        package_status= f'{organization.package_status}'
        package_start_date=f'{organization.package_start_date}'
        package_end_date = f'{organization.package_end_date}'
        creation_date = f'{organization.creation_date}'
        created_by = f'{organization.created_by}'
        last_update_date = f'{organization.last_update_date}'
        last_updated_by = f'{organization.last_updated_by}'
        last_update_login = f'{organization.last_update_login}'
        self.assertEqual(organization_id,'101')
        self.assertEqual(organization_name,'my_org')
        self.assertEqual(package_id,1)
        self.assertEqual(package_status, 1)
        self.assertEqual(package_start_date,datetime.date('01/01/2020'))
        self.assertEqual(package_end_date, datetime.date('01/01/2024'))
        self.assertEqual(creation_date,datetime.date('01/01/2018'))
        self.assertEqual(created_by,'oneuser')
        self.assertEqual(last_update_date,datetime.date('01/01/2022'))
        self.assertEqual(last_updated_by, 123)
        self.assertEqual(last_update_login, 123)
                
    def tests_create_new_organization_with_orgname_and_orgid_successfull(self):
        org_id=101
        org_name="inseyab"
        organization=get_organization_model().objects.create(organization_id=101, organization_name="inseyab")
        self.assertEqual(get_organization_model().objects.all().count(),1)
        self.assertEqual(organization.organization_id, org_id)
        self.assertEqual(organization.organigzation_name, org_name)
            
            
    # def test_no_duplicate_values_in_organization_id(self):
    #     unique_field_name= 'organization_id'
    #     instance1= Organization.objects.create({unique_field_name:'organization_id'})
    #     with self.assertRaises(IntegrityError):
    #         Organization.objects.create({unique_field_name:'organization_id'})
                
    def tests_package_validation(self):
        organization=Organization.objects.create(
        package_id = 101,
        package_status = 1,
        package_start_date ='1/1/2024',
        package_end_date ='1/1/2025',
        )
        self.assertLess(package_start_date, package_end_date)
        self.assertGreater(package_end_date, package_start_date)
        self.assertEqual(package_id, 101)
        self.assertEqual(package_status, 1)            
        
        
    def tests_organization_id_dealing_with_pk(self):
        organization = Organization.objects.create(
            organization_id = 101
        )
        with self.assertRaises(IntegrityError) as same_id:
            """create second org id with same id"""
            organization = Organization.objects.create(
                organization_id = 101
            )
        self.assertIn(organization_id,str(same_id,exception))    
            
                
        
    
    
    