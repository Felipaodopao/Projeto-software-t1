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