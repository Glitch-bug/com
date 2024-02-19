from django.test import TestCase 

from django.contrib.auth.models import User

from store.models import Category, Product, ProductType
from account.models import UserBase
class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name="django", slug="django")


    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model(self):
        data = self.data1
        self.assertEqual(str(data), 'django')

class TestProductsModel(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="django", slug="django")
        type = ProductType.objects.create(name="book", is_active=True)
        UserBase.objects.create_user(email='admin@admin.com', user_name="admin", password="think")
        self.data1 = Product.objects.create(category=cat, title="django beginners",
                                            slug='django-beginners', regular_price=20.00, discount_price=18.4, product_type=type)

    
    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')