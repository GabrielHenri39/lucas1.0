from django.test import TestCase,RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..views import cadastro

class TestCadastroView(TestCase):

    def  setUp(self):
        self.factory =  RequestFactory()
    
    def test_cadastro_get(self):
        """Teste: Acesso à rota de cadastro"""
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro.html')

    def test_cadastro_get_autenticado(self):
        user = get_user_model().objects.create_user(username='teste', password='senha1234')
        self.client.login(username='teste', password='senha1234')
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home')) 
         # Supondo que 'home' redirecione para a página principal

    def test_cadastro_post_valido(self):
        """Teste: Envio de dados válidos"""
        data = {'username': 'novo_usuario', 'email': 'novo@emails.com', 'senha': 'senha1223$A', 'confirmar_senha': 'senha1223$A'}

        request = self.factory.post(reverse('cadastro'), data)

        response = cadastro(request)

        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(get_user_model().objects.filter(username='novo_usuario').exists()) 
          
    
    def test_cadastro_post_invalido(self):
        """Teste: Envio de dados inválidos"""
        # Testar diversos cenários de dados inválidos
        # Exemplo: Usuário já existente

        data_invalida = {'username': 'teste', 'email': 'novo@emails.com', 'senha': 'senha1223$A', 'confirmar_senha': 'senha1223$A'}

        request = self.factory.post(reverse('cadastro'), data_invalida)

        response = cadastro(request)

        self.assertEqual(response.status_code, 302)  # Assumir que cadastro retorna 200 em caso de erro
        self.assertFalse(get_user_model().objects.filter(username='novo_usuario').exists())  # Verificar se usuário não foi criado

        # Verificar se mensagens de erro estão presentes na resposta (se aplicável)
        # ...
