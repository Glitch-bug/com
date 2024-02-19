from importlib import import_module
from unittest import skip

from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.models import User


from django.urls import reverse
from django.test import TestCase, Client, RequestFactory 


from store.views import product_all
from store.models import Category, Product, ProductType
from account.models import UserBase
@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_example(self):
        pass

class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        cat = Category.objects.create(name="django", slug="django")
        type = ProductType.objects.create(name="book", is_active=True)
        UserBase.objects.create_user(email='admin@admin.com', user_name="admin", password="think")
        self.data1 = Product.objects.create(category=cat, title="django beginners",
                                            slug='django-beginners', regular_price=20.00, discount_price=18.4, product_type=type)

    
    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/',)
        self.assertEqual(response.status_code, 200)
    

    def test_product_detail_url(self):
        """
        Test Product response status
        """
        response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)
    

    def test_product_list_url(self):
        """
        Test Category response status
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)
    

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<h1 class="h3">Popular</h1>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
    


        
    