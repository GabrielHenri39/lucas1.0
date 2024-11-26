from django.db import models
from pacientes.models  import Pacientes

# Create your models here.

class DiaDaSemana(models.Model):
     choices_dias_da_semana = (
        ('Segunda', 'Segunda'),
        ('Terça', 'Terça'),
        ('Quarta', 'Quarta'),
        ('Quinta', 'Quinta'),
        ('Sexta', 'Sexta'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    )

     dia = models.CharField(max_length=10, choices=choices_dias_da_semana)

     def __str__(self):
        return self.dia

     

class Horario(models.Model):
    horario = models.TimeField()

    def __str__(self):
        return f"{self.horario}"

class Atendimento(models.Model):
   
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    dias = models.ManyToManyField(to=DiaDaSemana)

    horarios = models.ManyToManyField(to=Horario)
   
    

    def __str__(self):
        return f"Atendimento de {self.paciente.nome} "
    

    def  get_dias(self):
        return ", ".join([dia.dia for dia in self.dias.all()])
    