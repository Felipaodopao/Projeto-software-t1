from django.db import models
from django.contrib.auth.models import User


class Tarefa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    data = models.DateField()
    concluida = models.BooleanField(default=False)

    class Meta:
        ordering = ['data']

    def __str__(self):
        return f"{self.descricao} ({self.data})"
    

class Humor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    nivel = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=20, blank=True)
    relato = models.TextField(blank=True)

    class Meta:
        unique_together = ('usuario', 'data')
        ordering = ['-data']

    def __str__(self):
        return f'{self.usuario.username} - {self.data} - Humor: {self.nivel}'
    
class Consulta(models.Model):
    TIPO_CHOICES = [
        ('psicologo', 'Psicólogo'),
        ('psicopedagogo', 'Psicopedagogo'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()  # <-- Adicione esta linha
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ['data']

    def __str__(self):
        return f"{self.get_tipo_display()} em {self.data} {self.hora} ({self.usuario.username})"
    
    
class Perfil(models.Model):
    USER_TYPE_CHOICES = [
        ('usuario', 'Usuário'),
        ('psicologo', 'Psicólogo'),
        ('psicopedagogo', 'Psicopedagogo'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='usuario')

    def __str__(self):
        return f"{self.user.username} ({self.get_tipo_display()})"
    
class Disponibilidade(models.Model):
    profissional = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    disponivel = models.BooleanField(default=True)

    class Meta:
        unique_together = ('profissional', 'data', 'hora')
        ordering = ['data', 'hora']

    def __str__(self):
        return f"{self.profissional.username} - {self.data} {self.hora} - {'Disponível' if self.disponivel else 'Indisponível'}"