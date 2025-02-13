import re
from django.contrib import messages
from django.contrib.messages import constants
import logging 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)

def password_is_valid(password, confirm_password, request=None):
    """
    Verifica se a senha é válida e adiciona mensagens para o usuário.

    Parâmetros:
    password -- A senha a ser validada
    confirm_password -- A confirmação da senha
    request -- O objeto request da view

    Retorna:
    True se a senha for válida, False caso contrário
    """

    # if type(password) == WSGIRequest and type(confirm_password) == WSGIRequest:
    #     password = password.POST.get('confirmar_senha')
    #     confirm_password = confirm_password.POST.get('confirm_password')
        
    
    # senhar não poder  ser vazia
    if not password or not confirm_password:
        messages.add_message(request, constants.ERROR, 'A senha não pode ser vazia.')
        logger.error(' O usuario tentou cadastrar uma senha vazia')
        return False
 
    
    if not re.match('^.{8,}$',password):

        messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos 8 caracteres.')
        logger.error('Senha inválida: menos de 8 caracteres')
        return False

    if not password.strip() == confirm_password.strip():
        messages.add_message(request,constants.ERROR, 'As senhas não conferem.')
        logger.error('As senhas não conferem: a confirmação da senha não corresponde à senha original')
        return False

    if not re.search(r'[A-Z]', password.strip()):
        messages.add_message(request, constants.ERROR,'A senha deve conter pelo menos uma letra maiúscula.')
        logger.error('Senha inválida: falta de letra maiúscula')
        
        return False

    if not re.search(r'[a-z]', password.strip()):
        messages.add_message(request, constants.ERROR,'A senha deve conter pelo menos uma letra minúscula.')
        
        logger.error('Senha inválida: falta de letra minúscula')
        return False

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password.strip()):
        messages.add_message(request, constants.ERROR,'A senha deve conter pelo menos um caractere especial.')
        logger.error('Senha inválida: falta de caractere especial')
        return False
    
    if not re.search(r'[0-9]',password.strip()):
        messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos um número.')
        logger.error('Senha inválida: falta de número')
        return False

    if re.match(r'[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}', password.strip()):
        messages.add_message(request, constants.ERROR,'A senha não pode ser uma data de nascimento.')
        logger.error('Senha inválida: formato de data de nascimento')
        return False

    if re.match(r'[0-9]{1,3}[-_ ][0-9]{1,3}[-_ ][0-9]{1,3}', password.strip()):
        messages.add_message(request, constants.ERROR,'A senha não pode ser uma sequência de números.')

        logger.error('Senha inválida: formato de sequência de números')
        return False

    
    return True


def send_password_reset_email(user, reset_token):
    subject = "Redefinição de senha - Django"
    email_template_name = "password_reset_email.html"
    
    try:
        html_content = render_to_string(email_template_name,{"user": user,"reset_token": reset_token})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[user.email])
        email.attach_alternative(html_content,'text/html')
        email.send()

        logger.info("E-mail de redefinição de senha enviado com sucesso")

        return True
    except:
        logger.error("Erro ao enviar e-mail de redefinição de senha")
        return False