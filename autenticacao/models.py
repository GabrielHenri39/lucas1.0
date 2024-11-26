from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.urls import reverse



# Create your models here.

class User(AbstractUser):
    """ 
    Modelo de usuario personalizado 

    """
    is_fisioterapeuta =  models.BooleanField(default=False,verbose_name='Fisioterapeuta')
    email =  models.EmailField(unique=True,blank=True,null=True)



    
class LoginAttempt(models.Model):
    """

    Modelo de intento de inicio de sesión

    """
    username = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)


class ResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True) 


    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=32) 

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('password_reset_confirm', args=[self.user.pk, self.token])