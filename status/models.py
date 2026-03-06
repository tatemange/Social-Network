from django.db import models
from django.conf import settings

class Statut(models.Model):
    TYPE_CHOICES = (
        ('texte', 'Texte'),
        ('image', 'Image'),
        ('video', 'Vidéo'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='statuts', on_delete=models.CASCADE, db_column='idUser')
    typeStatut = models.CharField(max_length=10, choices=TYPE_CHOICES, db_column='type')
    contenu = models.TextField(null=True, blank=True)
    datePublication = models.DateTimeField(auto_now_add=True)
    dateExpiration = models.DateTimeField()

    class Meta:
        verbose_name = 'Statut'
        verbose_name_plural = 'Statuts'
        db_table = 'Statut'

    def __str__(self):
        return f"Statut by {self.user} - Expirant le {self.dateExpiration}"
