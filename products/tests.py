from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Category, Product

User = get_user_model()


class ProductAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='123456')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Electrónica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price='15000.00',
        )

    def test_create_category(self):
        response = self.client.post(
            reverse('categories-list'),
            {'name': 'Ropa'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(name='Ropa').count(), 1)

    def test_list_categories(self):
        response = self.client.get(reverse('categories-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        response = self.client.post(
            reverse('product-list'),
            {
                'name': 'Mouse',
                'category': self.category.id,
                'description': 'Mouse inalámbrico',
                'price': '500.00',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.filter(name='Mouse').count(), 1)

    def test_list_products(self):
        response = self.client.get(reverse('product-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_product(self):
        response = self.client.put(
            reverse('product-detail', args=[self.product.id]),
            {
                'name': 'Laptop Pro',
                'category': self.category.id,
                'description': 'Laptop HP actualizada',
                'price': '18000.00',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')
        self.assertEqual(float(self.product.price), 18000.00)

    def test_delete_product(self):
        response = self.client.delete(reverse('product-detail', args=[self.product.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_precio_final_autenticado(self):
        response = self.client.get(
            reverse('producto-precio-final', args=[self.product.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('precio_final', response.data)
        self.assertEqual(response.data['precio_final'], 13500.00)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse('producto-precio-final', args=[self.product.id])
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
