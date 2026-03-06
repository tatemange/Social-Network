from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=50)
    numero_telephone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    photoProfil = models.ImageField(upload_to='profiles/', null=True, blank=True)
    dateCreation = models.DateTimeField(auto_now_add=True)
    statutEnLigne = models.BooleanField(default=False)
    
    # Required for custom user model
    USERNAME_FIELD = 'numero_telephone'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'


class Contact(models.fields.Field):
    # This is a bit of a hack to avoid circular dependencies and just represent the relation
    pass

class ContactRelation(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts_user2', on_delete=models.CASCADE)
    dateAjout = models.DateTimeField(auto_now_add=True)
    bloque = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user1', 'user2')
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def clean(self):
        if self.user1.id and self.user2.id:
            if self.user1.id >= self.user2.id:
                raise ValidationError(_("user1's ID must be less than user2's ID to enforce symmetric uniqueness."))

    def save(self, *args, **kwargs):
        # We enforce the constraint ID sorting before saving
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Contact {self.user1} - {self.user2}"
