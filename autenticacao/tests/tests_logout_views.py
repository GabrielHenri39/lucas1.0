from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestLogoutView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='senha1234')

    def test_logout(self):
        """Teste: Logout do usuário"""
        self.client.login(username='test', password='senha1234')
        response = self.client.get(reverse('sair'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))  # Supondo que 'login' redirecione para a página login
        self.assertFalse(self.client.session.has_key('_auth_user_id'))  # Verifica se o usuário foi deslogado