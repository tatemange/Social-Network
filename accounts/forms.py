from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('numero_telephone', 'nom', 'prenom', 'email', 'photoProfil')
        
        pill_css = 'w-full bg-transparent border border-gray-300 dark:border-gray-800 text-gray-900 dark:text-white text-sm rounded-full px-6 py-4 focus:outline-none focus:ring-1 focus:ring-blue-600 focus:border-blue-600'
        
        widgets = {
            'numero_telephone': forms.TextInput(attrs={'class': pill_css, 'placeholder': 'Numéro de téléphone', 'type': 'tel'}),
            'nom': forms.TextInput(attrs={'class': pill_css, 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': pill_css, 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': pill_css, 'placeholder': 'Adresse email (facultatif)'}),
            'photoProfil': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-6 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100 dark:file:bg-gray-800 dark:file:text-gray-300'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Translation and simplification of password help texts
        if 'password1' in self.fields:
            self.fields['password1'].help_text = "Votre mot de passe doit comporter au moins 8 caractères."
        if 'password2' in self.fields:
            self.fields['password2'].label = "Confirmation du mot de passe"
            self.fields['password2'].help_text = "Veuillez saisir le même mot de passe."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.numero_telephone
        if commit:
            user.save()
        return user
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('numero_telephone', 'nom', 'prenom', 'email', 'photoProfil')
        
        pill_css = 'w-full bg-transparent border border-gray-300 dark:border-gray-800 text-gray-900 dark:text-white text-sm rounded-full px-6 py-4 focus:outline-none focus:ring-1 focus:ring-blue-600 focus:border-blue-600'

        widgets = {
            'numero_telephone': forms.TextInput(attrs={'class': pill_css, 'placeholder': 'Numéro de téléphone', 'type': 'tel'}),
            'nom': forms.TextInput(attrs={'class': pill_css, 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': pill_css, 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': pill_css, 'placeholder': 'Adresse email (facultatif)'}),
            'photoProfil': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-6 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100 dark:file:bg-gray-800 dark:file:text-gray-300'}),
        }
