from django.db import models
from django.contrib.auth.models import User

class Humor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    nivel = models.IntegerField()  # Valor de 0 a 100, por exemplo
    relato = models.TextField(blank=True)

    class Meta:
        unique_together = ('usuario', 'data')
        ordering = ['-data']

    def __str__(self):
        return f'{self.usuario.username} - {self.data} - Humor: {self.nivel}'