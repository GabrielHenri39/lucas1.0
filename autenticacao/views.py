from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import constants
import logging
from .ultis import password_is_valid, send_password_reset_email
from .models import User, ResetToken
from django.db.transaction import atomic
from django.db import DatabaseError
from django.contrib.auth.hashers import make_password
from .form import LoginForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.conf import settings

# Create your views here.

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s: %(message)s', datefmt="%d/%m/%Y-%H:%M:%S")


def login(request):  # testando
    '''
    Função responsável por lidar com a requisição de login de usuário.
    :param request: objeto de requisição
    :return: renderização da página de login ou redirecionamento para a página inicial

    '''
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        form = LoginForm()

        return render(request, 'login.html', {'form': form})

    elif request.method == "POST":

        form = LoginForm(request.POST)

        if not form.is_valid():
            messages.add_message(request, constants.ERROR,
                                 'Usuário ou senha inválidos')
            return redirect(reverse('login'))

        else:
            username = form.cleaned_data.get('username')
            senha = form.cleaned_data.get('password')

        try:
            user = auth.authenticate(username=username, password=senha)

            if user is None:
                messages.add_message(
                    request, constants.ERROR, "Usuário ou senha inválidos")
                logger.error('')

                return render(request, 'login.html')

            else:

                auth.login(request, user)
                return redirect(reverse('home'))

        except Exception as e:
            messages.add_message(
                request, constants.ERROR, 'Ocorreu um erro durante o login. Tente novamente.')
            logger.error('An error occurred during login: %s', e)

        return render(request, 'login.html')


def cadastro(request: HttpRequest):
    """
    Função responsável por lidar com a requisição de cadastro de usuário.
    :param request: objeto de requisição
    :return: renderização da página de cadastro ou redirecionamento para a página inicial
    """

    if request.method == "GET":

        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        con_password = request.POST.get('confirmar_senha')

        with atomic():
            try:
                if not password_is_valid(password=password, confirm_password=con_password, request=request):
                    return redirect(reverse('cadastro'))

                user, create = User.objects.get_or_create(
                    username=username,
                    email=email,
                    defaults={'password': make_password(password)}
                )

                if not create:
                    messages.add_message(
                        request, constants.ERROR, 'Já existe um usuário com esse e-mail ou usuário')

                    return redirect(reverse('cadastro'))

                return redirect(reverse('login'))
            except DatabaseError as e:
                messages.add_message(
                    request, constants.ERROR, 'Ocorreu um erro durante o cadastro. Tente novamente.')
                logger.error('An error occurred during registration: %s', e)


def logout(request):
    """  
    Função responsável por lidar com a requisição de logout de usuário.
    :param request: objeto de requisição
    :return: redirecionamento para a página de login
    """
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    auth.logout(request)

    return redirect(reverse('login'))


def password_reset_request(request):
    """
    Função responsável por lidar com a requisição de reset de senha de usuário.
    :param request: objeto de requisição
    :return: renderização da página de reset de senha ou redirecionamento para a página de login
    """
    if request.method == "GET":
        form = CustomPasswordResetForm()
        return render(request, 'password_reset.html', {'form': form})

    elif request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            users = get_user_model().objects.filter(email__iexact=email).first()
            if users is not None:
                reset_token = PasswordResetTokenGenerator().make_token(users)
                uidb64 = urlsafe_base64_encode(str(users.pk).encode('utf-8'))
                url_abilute = f'{
                    settings.SITE_URL}auth/reset/{uidb64}/{reset_token}'
                send_password_reset_email(users, url_abilute)

            messages.add_message(
                request, constants.INFO, 'Um e-mail de redefinição de senha foi enviado para o seu endereço de e-mail.')
            return redirect(reverse('login'))
        else:
            messages.add_message(
                request, constants.ERROR, 'Ocorreu um erro durante a solicitação de redefinição de senha. Tente novamente.')
            return redirect(reverse('password_reset'))


def password_reset_confirm(request, uidb64, token):
    """
    Função responsável por lidar com a requisição de confirmação de reset de senha de usuário.
    :param request: objeto de requisição
    :param uidb64: uidb64
    :param token: token
    :return: renderização da página de confirmação de reset de senha ou redirecionamento para a página de login
    """
    if request.method == "GET":
        form = CustomSetPasswordForm(user=request.user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    user = User.objects.filter(
        pk__exact=int(urlsafe_base64_decode(uidb64)),

    ).first()
    if user is not None:
        if request.method == "POST":
            form = CustomSetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                senha = form.cleaned_data.get('new_password1')
                user.password = make_password(senha)

                user.save()
                logger.info(
                    'Password reset successful for user %s', user.username)
                return redirect(reverse('password_reset_complete'))
            else:
                return render(request, 'password_reset_confirm.html', {'form': form})


def password_reset_complete(request):
    """
    Função responsável por renderizar a página de reset de senha concluído com sucesso.
    :param request: objeto de requisição
    :return: renderização da página de reset de senha concluído com sucesso
    """
    return render(request, 'password_reset_complete.html')
