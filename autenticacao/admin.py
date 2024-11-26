from django.contrib import admin
from .models import User,ResetToken
from django.contrib.auth import admin as admin_auth
from .form import CustomUserChangeForm, CustomUserCreationForm


admin.site.register(ResetToken)

@admin.register(User)
class UsersAdmin(admin_auth.UserAdmin):
    """ Admin para o modelo User"""
    
    form = CustomUserChangeForm
    list_display = ('username', 'is_fisioterapeuta')
    list_filter= ('is_fisioterapeuta','is_active','is_staff','is_superuser')
    add_form = CustomUserCreationForm
    model = User
    fieldsets = admin_auth.UserAdmin.fieldsets + (
        ("Campos Personalizados", {"fields": ("is_fisioterapeuta",)}),
    ) # type: ignore
    
    

    def get_form(self, request, obj=None, **kwargs):
        help_text = "Atributo booleano que indica se o usuário é um Fisoyerapeuta ou não."
        kwargs.update({"help_texts": {"is_fisioterapeuta": help_text}})
        return super().get_form(request, obj, **kwargs)

     
   