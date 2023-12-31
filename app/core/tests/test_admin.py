"""
Test for django admin modification
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Organization, Package, UserRole


class AdminSiteTest(TestCase):
    """Test for django admin"""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            "admin@example.com",
            'testpass123'
        )
        self.client.force_login(self.admin_user)
        self.organization = Organization.objects.create(
            name="Test Organization"
            )
        Package.objects.create(name='basic')
        UserRole.objects.create(name='admin')
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password='testpass123',
            organization=self.organization,
        )

    def test_user_list(self):
        """Test that users are listed on the page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.organization)
        self.assertContains(res, self.user.package)
        self.assertContains(res, self.user.role)

    def test_edit_user_page(self):
        """Test edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
