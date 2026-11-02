from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='cliente1',
            email='cliente1@tiendaonline.com',
            password='Clave1234!',
            telefono='55512345',
        )
        self.admin = User.objects.create_superuser(
            username='admin2',
            email='admin2@tiendaonline.com',
            password='Admin1234!',
        )

    def authenticate(self, email, password):
        response = self.client.post(
            reverse('token_obtain_pair'), {'email': email, 'password': password}
        )
        return response

    def test_login_by_email_returns_access_and_refresh(self):
        response = self.authenticate('cliente1@tiendaonline.com', 'Clave1234!')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_me_endpoint_returns_data_without_password(self):
        access = self.authenticate('cliente1@tiendaonline.com', 'Clave1234!').data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.get(reverse('user-me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'cliente1@tiendaonline.com')
        self.assertEqual(response.data['telefono'], '55512345')
        self.assertNotIn('password', response.data)

    def test_admin_list_and_detail_dont_expose_password(self):
        access = self.authenticate('admin2@tiendaonline.com', 'Admin1234!').data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

        list_response = self.client.get(reverse('user-list'))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        for item in list_response.data:
            self.assertNotIn('password', item)

        detail_response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', detail_response.data)

    def test_patch_and_put_without_password_dont_change_hash(self):
        access = self.authenticate('admin2@tiendaonline.com', 'Admin1234!').data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        original_hash = self.user.password

        patch_response = self.client.patch(
            reverse('user-detail', args=[self.user.id]), {'telefono': '55599999'}
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, original_hash)

        put_response = self.client.put(
            reverse('user-detail', args=[self.user.id]),
            {
                'username': self.user.username,
                'email': self.user.email,
                'first_name': '',
                'last_name': '',
                'telefono': '55588888',
                'is_active': True,
                'is_staff': False,
            },
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, original_hash)

        login_response = self.authenticate('cliente1@tiendaonline.com', 'Clave1234!')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_patch_with_password_changes_hash_and_allows_new_login(self):
        access = self.authenticate('admin2@tiendaonline.com', 'Admin1234!').data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        original_hash = self.user.password

        response = self.client.patch(
            reverse('user-detail', args=[self.user.id]), {'password': 'NuevaClave1234!'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, original_hash)

        old_login = self.authenticate('cliente1@tiendaonline.com', 'Clave1234!')
        self.assertEqual(old_login.status_code, status.HTTP_401_UNAUTHORIZED)

        new_login = self.authenticate('cliente1@tiendaonline.com', 'NuevaClave1234!')
        self.assertEqual(new_login.status_code, status.HTTP_200_OK)

    def test_access_token_lifetime_is_30_minutes(self):
        self.assertEqual(
            settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], timedelta(minutes=30)
        )
