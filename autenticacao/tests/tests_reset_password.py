from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestsResetPassword(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            email='test@example.com',
            password='senha1223$A'
        )

    def test_reset_password_view(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')

    def test_reset_password_done_view(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')

    def test_reset_password_confirm_view(self):
        response = self.client.get(reverse('password_reset_confirm', args=['uidb64', 'token']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_confirm.html')

    def test_reset_password_complete_view(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_complete.html')