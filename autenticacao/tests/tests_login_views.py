from django.test import TestCase,RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..views import cadastro


class TestLoginView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='teste', password='senha1234')

    def test_login_get_autenticado(self):
        """Teste: Usuário autenticado acessando a rota de login"""
        self.client.login(username='teste', password='senha1234')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))  # Supondo que 'home' redirecione para a página principal

    def test_login_get_nao_autenticado(self):
        """Teste: Usuário não autenticado acessando a rota de login"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_valido(self):
        """Teste: Envio de credenciais válidas"""
        data = {'username': 'teste', 'password': 'senha1234'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))  # Supondo que 'home' redirecione para a página principal
        self.assertTrue(self.client.session.has_key('_auth_user_id'))  # Verifica se o usuário está logado

    def test_login_post_invalido(self):
        """Teste: Envio de credenciais inválidas"""
        data = {'username': 'inexistente', 'password': 'qualquer'}
        response = self.client.post(reverse('login'), data, content_type="application/x-www-form-urlencoded")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))  # Supondo que 'login' redirecione para a página de login

        self.assertTrue(len(self.client.session.items()) == 0)  # Verifica se o usuário não está logado


        
