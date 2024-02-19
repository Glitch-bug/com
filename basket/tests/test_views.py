from account.models import UserBase
from django.test import TestCase 
from django.urls import reverse 

from store.models import Category, Product, ProductType

class TestBasketView(TestCase):
    def setUp(self):
        UserBase.objects.create_user(email='admin@admin.com', user_name="admin", password="think")
        cat = Category.objects.create(name="django", slug="django")
        type = ProductType.objects.create(name="book", is_active=True)
        self.data1 = Product.objects.create(category=cat, title="django beginners",
                                            slug='django-beginners', regular_price=20.00, discount_price=18.4, product_type=type)
        self.data2 = Product.objects.create(category=cat, title="django intermediary",
                                            slug='django-intermediary', regular_price=30.00, discount_price=18.4, product_type=type)
       
        self.data3 = Product.objects.create(category=cat, title="django advanced",
                                            slug='django-advanced', regular_price=40.00, discount_price=18.4, product_type=type)

        self.client.post(
            reverse('basket:basket_add'), {"productid":1, "productqty":1, "action":"post"}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {"productid":2, "productqty":2, "action":"post"}, xhr=True
        )

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse('basket:basket_add'), {"productid":3, "productqty":1, "action":"post"}, xhr=True)
        self.assertEqual(response.json(), {'qty':4})
        response = self.client.post(
            reverse('basket:basket_add'), {"productid":2, "productqty":1, "action":"post"}, xhr=True)
        self.assertEqual(response.json(), {'qty':3})
    
    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_delete'), {"productid":2, "action":"post"}, xhr=True
        )
        self.assertEqual(response.json(), {'qty':1, 'subtotal':'20.00'})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_update'), {"productid":2, "productqty":1, "action":"post"}, xhr=True
        )
        self.assertEqual(response.json(), {'qty':2, 'subtotal':'50.00'})