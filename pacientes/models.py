from django.db import models
from datetime import date
# Create your models here.

class Pacientes(models.Model):

    choice_sexo = (
        ("F", "Feminino"),
        ("M", "Masculino"),
    )

    nome =  models.CharField(max_length=100)
    data_nascimento  = models.DateField()
    sexo = models.CharField(max_length=1,choices=choice_sexo)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    ficha_criada = models.DateTimeField(auto_now_add=True)
    ficha_atualizada = models.DateTimeField(auto_now=True)
    
    @property
    def ficha_criada_formt(self):

        return self.ficha_criada.strftime('%d/%m/%Y %H:%M:%S')

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age
    class Meta:
        verbose_name_plural = 'Pacientes'
    
class FichaMedica(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, related_name='fichas')
    
    alergias = models.TextField(blank=True,null=True)
    cirurgias = models.TextField(blank=True,null=True)
    doenca = models.TextField(blank=True,verbose_name='doença',null=True)
    diagnostico = models.TextField(blank=True,null=True)
    observacoes = models.TextField(blank=True,null=True,verbose_name='Observações')
    quexa_pricipal = models.TextField(blank=True,null=True)
    quexa_secundaria = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.paciente.nome
    
    
    class  Meta:
        verbose_name_plural = 'Fichas Médicas'

class EVA(models.Model):
    choioice_eva = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
    )
    ficha = models.ForeignKey(FichaMedica, on_delete=models.CASCADE, related_name='evas')
    data = models.DateField()

    eva = models.CharField(max_length=2, choices=choioice_eva)

    def __str__(self):
        return f"EVA de {self.ficha.paciente.nome} em {self.data}"
    class  Meta:
        verbose_name_plural = 'Evas'
    


class Evolucao(models.Model):
    ficha = models.ForeignKey(FichaMedica, on_delete=models.CASCADE, related_name='evolucoes')
    data = models.DateField(auto_now_add=True)
    peso = models.DecimalField(verbose_name='Peso',decimal_places=2,max_digits=5)
    altura = models.DecimalField(verbose_name='Altura', decimal_places=2,max_digits=3)
    pressao_sislotica = models.PositiveIntegerField(verbose_name='Pressão Sislótica')
    pressao_diastolica = models.PositiveIntegerField(verbose_name='Pressão Diastólica')
    evolucao = models.TextField(verbose_name='Evolução')

    def __str__(self):
        return f"Evolução de {self.ficha.paciente.nome} em {self.data}"
    
    @property
    def  pressao(self):
        return f"{self.pressao_sislotica}/{self.pressao_diastolica} mmHg"
    
    @property
    def imc(self):
        return self.peso / (self.altura * self.altura)
    class   Meta:
        verbose_name_plural = 'Evoluções'