from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Compte créé avec succès. Bienvenue {user.prenom}!")
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # set status online
                user.statutEnLigne = True
                user.save()
                
                messages.success(request, f"Bienvenue de retour, {user.prenom}!")
                return redirect('/')
            else:
                messages.error(request, "Email ou mot de passe invalide.")
        else:
            messages.error(request, "Email ou mot de passe invalide.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    user = request.user
    user.statutEnLigne = False
    user.save()
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('accounts:login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

from django.http import JsonResponse
from django.db.models import Q
from .models import ContactRelation

@login_required
def add_contact(request, user_id):
    if request.method == 'POST':
        if request.user.id == user_id:
            return JsonResponse({'status': 'error', 'message': "Cannot add yourself."}, status=400)
        
        try:
            target_user = CustomUser.objects.get(id=user_id)
            u1, u2 = (request.user, target_user) if request.user.id < target_user.id else (target_user, request.user)
            contact, created = ContactRelation.objects.get_or_create(user1=u1, user2=u2)
            if not created and contact.bloque:
                return JsonResponse({'status': 'error', 'message': "Contact is blocked."}, status=400)
            return JsonResponse({'status': 'success', 'message': "Contact added."})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "User not found."}, status=404)
    return JsonResponse({'status': 'error', 'message': "Invalid method."}, status=405)

@login_required
def block_contact(request, user_id):
    if request.method == 'POST':
        try:
            target_user = CustomUser.objects.get(id=user_id)
            u1, u2 = (request.user, target_user) if request.user.id < target_user.id else (target_user, request.user)
            contact, created = ContactRelation.objects.get_or_create(user1=u1, user2=u2)
            contact.bloque = True
            contact.save()
            return JsonResponse({'status': 'success', 'message': "Contact blocked."})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "User not found."}, status=404)
    return JsonResponse({'status': 'error', 'message': "Invalid method."}, status=405)

@login_required
def add_contact_by_phone(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            phone = data.get('numero_telephone')
            if not phone:
                return JsonResponse({'status': 'error', 'message': "Numéro de téléphone requis."}, status=400)
            
            target_user = CustomUser.objects.get(numero_telephone=phone)
            
            if request.user.id == target_user.id:
                return JsonResponse({'status': 'error', 'message': "Vous ne pouvez pas vous ajouter vous-même."}, status=400)
                
            u1, u2 = (request.user, target_user) if request.user.id < target_user.id else (target_user, request.user)
            contact, created = ContactRelation.objects.get_or_create(user1=u1, user2=u2)
            if not created and contact.bloque:
                return JsonResponse({'status': 'error', 'message': "Ce contact est bloqué."}, status=400)
            return JsonResponse({'status': 'success', 'message': "Contact ajouté avec succès."})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "Aucun utilisateur trouvé avec ce numéro."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': "Données invalides."}, status=400)
    return JsonResponse({'status': 'error', 'message': "Invalid method."}, status=405)
