from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordResetForm,SetPasswordForm # type: ignore
from .models import User

    
class CustomUserCreationForm(UserCreationForm):
    """
    Formulário de criação de usuário personalizado.
    Inclui campos adicionais para nome, sobrenome, email e senha.
    Também inclui campos para especificar se o usuário é médico ou não.
    """
    

    class Meta(UserCreationForm.Meta): # type: ignore
        model = User
        fields = UserCreationForm.Meta.fields  + ('is_fisioterapeuta', ) # type: ignore
        filter =  ('is_fisioterapeuta',)
        

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta): # type: ignore
        model = User
        fields = UserChangeForm.Meta.fields # type: ignore



class LoginForm(forms.Form):
    username = forms.CharField(label='Username',required=True,widget=forms.TextInput(attrs={'class':"input"}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'input'}), required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuário não encontrado')
        return username
    def  clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Senha incorreta')
        user = User.objects.get(username=username)
        if not user.check_password(password): # type: ignore
            raise forms.ValidationError('Senha incorreta')
        return password

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'input'}))
    

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Nova senha", widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password2 = forms.CharField(label="Confirme a nova senha", widget=forms.PasswordInput(attrs={'class': 'input'}))    