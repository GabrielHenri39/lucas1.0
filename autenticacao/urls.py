from django.urls import path
from autenticacao import views


urlpatterns = [
    path('login/', views.login, name='login'),  # type: ignore
    path('cadastro/', views.cadastro, name="cadastro"),  # type: ignore
    path('password_reset/', views.password_reset_request, # type: ignore
         name="password_reset"),  # type: ignore
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, # type: ignore
         name="password_reset_confirm"),  # type: ignore
    path('password_reset_complete/', views.password_reset_complete,
         name="password_reset_complete"),
    path('sair/', views.logout, name='sair'),

]
