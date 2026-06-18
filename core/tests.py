from decimal import Decimal

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from . import views
from .models import Product


class ProductFlowTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(username='owner', password='secure-pass-123')
        self.other_user = User.objects.create_user(username='other', password='secure-pass-123')
        self.active_product = Product.objects.create(
            name='Active Product',
            description='Ready for buyers.',
            price=Decimal('19.99'),
            created_by=self.owner,
            active=True,
        )
        self.inactive_product = Product.objects.create(
            name='Inactive Product',
            description='Still in progress.',
            price=Decimal('29.99'),
            created_by=self.owner,
            active=False,
        )

    def request(self, method, path, user=None, data=None):
        request = getattr(self.factory, method)(path, data=data or {})
        request.user = user or AnonymousUser()

        SessionMiddleware(lambda req: None).process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)
        return request

    def test_product_list_only_shows_active_products(self):
        request = self.request('get', reverse('product_list'))

        response = views.product_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.active_product.name)
        self.assertNotContains(response, self.inactive_product.name)

    def test_anonymous_user_cannot_view_inactive_product(self):
        request = self.request('get', reverse('product_detail', args=[self.inactive_product.pk]))

        with self.assertRaises(Http404):
            views.product_detail(request, self.inactive_product.pk)

    def test_owner_can_view_and_update_inactive_product(self):
        detail_request = self.request(
            'get',
            reverse('product_detail', args=[self.inactive_product.pk]),
            user=self.owner,
        )
        detail_response = views.product_detail(detail_request, self.inactive_product.pk)

        self.assertEqual(detail_response.status_code, 200)

        update_request = self.request(
            'post',
            reverse('product_update', args=[self.inactive_product.pk]),
            user=self.owner,
            data={
                'name': 'Updated Product',
                'description': 'Ready now.',
                'price': '39.99',
                'active': 'on',
            },
        )
        update_response = views.product_update(update_request, self.inactive_product.pk)

        self.assertEqual(update_response.status_code, 302)
        self.assertEqual(update_response['Location'], self.inactive_product.get_absolute_url())
        self.inactive_product.refresh_from_db()
        self.assertEqual(self.inactive_product.name, 'Updated Product')
        self.assertTrue(self.inactive_product.active)

    def test_non_owner_cannot_update_product(self):
        request = self.request(
            'post',
            reverse('product_update', args=[self.active_product.pk]),
            user=self.other_user,
            data={
                'name': 'Taken Over',
                'description': 'Nope.',
                'price': '9.99',
                'active': 'on',
            },
        )

        with self.assertRaises(Http404):
            views.product_update(request, self.active_product.pk)
        self.active_product.refresh_from_db()
        self.assertEqual(self.active_product.name, 'Active Product')

    def test_create_product_requires_login(self):
        request = self.request('get', reverse('product_create'))

        response = views.product_create(request)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_owner_can_delete_product(self):
        request = self.request(
            'post',
            reverse('product_delete', args=[self.active_product.pk]),
            user=self.owner,
        )

        response = views.product_delete(request, self.active_product.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('dashboard'))
        self.assertFalse(Product.objects.filter(pk=self.active_product.pk).exists())
