from django.db import models
from django.conf import settings

class Discussion(models.fields.Field):
    pass

class Conversation(models.Model):
    TYPE_CHOICES = (
        ('prive', 'Privé'),
        ('groupe', 'Groupe'),
    )
    type_conv = models.CharField(max_length=10, choices=TYPE_CHOICES)
    dateCreation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Discussion'
        verbose_name_plural = 'Discussions'
        db_table = 'Discussion'


class Participant(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('membre', 'Membre'),
    )
    discussion = models.ForeignKey(Conversation, related_name='participants', on_delete=models.CASCADE, db_column='idDiscussion')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='discussions_participated', on_delete=models.CASCADE, db_column='idUser')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='membre')
    dateAjout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        unique_together = ('discussion', 'user')
        db_table = 'Participant'


class Groupe(models.Model):
    discussion = models.OneToOneField(Conversation, primary_key=True, on_delete=models.CASCADE, db_column='idDiscussion')
    nom = models.CharField(max_length=80)
    photo = models.ImageField(upload_to='group_profiles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Groupe'
        verbose_name_plural = 'Groupes'
        db_table = 'Groupe'


class Message(models.Model):
    TYPE_CHOICES = (
        ('texte', 'Texte'),
        ('image', 'Image'),
        ('video', 'Vidéo'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    )
    discussion = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE, db_column='idDiscussion')
    expediteur = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_sent', on_delete=models.CASCADE, db_column='idExpediteur')
    contenu = models.TextField(null=True, blank=True)
    typeMessage = models.CharField(max_length=20, choices=TYPE_CHOICES)
    dateEnvoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        db_table = 'Message'


class MessageStatut(models.Model):
    STATUT_CHOICES = (
        ('envoye', 'Envoyé'),
        ('recu', 'Reçu'),
        ('lu', 'Lu'),
    )
    message = models.ForeignKey(Message, related_name='statuts', on_delete=models.CASCADE, db_column='idMessage')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_statuts', on_delete=models.CASCADE, db_column='idUser')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    dateStatut = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Statut de Message'
        verbose_name_plural = 'Statuts de Message'
        unique_together = ('message', 'user')
        db_table = 'MessageStatut'


class Document(models.Model):
    message = models.ForeignKey(Message, related_name='documents', on_delete=models.CASCADE, db_column='idMessage')
    nomFichier = models.CharField(max_length=150)
    urlFichier = models.FileField(upload_to='chat_documents/')
    taille = models.BigIntegerField()
    format = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        db_table = 'Document'
