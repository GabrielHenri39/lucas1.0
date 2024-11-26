from django.contrib import admin
from .models import *

@admin.register(Pacientes)
class PacientesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'data_nascimento', 'endereco')
    search_fields = ('nome', 'telefone', 'email', 'endereco')
    list_filter = ('nome', 'telefone', 'email', 'data_nascimento', 'endereco')
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'telefone', 'email', 'data_nascimento', 'endereco','sexo')
        }),
        
    )

    ordering = ('nome',)
    
    

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'






@admin.register(EVA)

class EVASAdmin(admin.ModelAdmin):
    list_display = ('ficha', 'data',  )
    search_fields = ('FichaMedica__pacientes__nome', 'data' )
    list_filter = ('ficha', 'data', )
    ordering = ('data', )
    fieldsets = (
        ('Informações da EVA', {
            'fields': ('ficha', 'data', 'eva' )
        }),
    )

    class Meta:
        verbose_name = 'EVA'
        verbose_name_plural = 'Evas'

@admin.register(FichaMedica)
class FichaMedicaAdmin(admin.ModelAdmin):
    list_display = ('paciente', )
    search_fields = ('pacientes__nome', )
    list_filter = ('paciente', )
    ordering = ()
    fieldsets = (
        ('Informações ', {
            'fields': ('paciente', )
        }),
        ('Informações Médicas',{

            'fields': ('alergias', 'cirurgias', 'doenca', 'diagnostico', 'observacoes', 'quexa_pricipal', 'quexa_secundaria', )
        }),
    )

    class Meta:
        verbose_name = 'Ficha Médica'
        verbose_name_plural = 'Fichas Médicas'

#admin
@admin.register(Evolucao)
class EvolucaoAdmin(admin.ModelAdmin):
    list_display = ('ficha', 'data',)
    readonly_fields  = ('data',)
    search_fields = ('ficha__paciente__nome',)
    list_filter = ('ficha', 'data',)
    ordering = ('ficha','-data')
    fieldsets = (
        ('Informações do dia da Evolução', {
            'fields': ('ficha', 'data',)
        }),

        ('Informações da Evolução', {
            'fields': ('evolucao','peso','altura','pressao_sislotica','pressao_diastolica')
        }),
    )

    class Meta:
        verbose_name = 'Evolução'
        verbose_name_plural = 'Evoluções'


# Register your models here.
