from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
import json
from accounts.models import CustomUser, ContactRelation
from .models import Conversation, Participant

@login_required
def index(request):
    # Fetch all users except the current one
    # A real app might only fetch contacts here
    # We will fetch users to allow starting a new chat easily
    users = CustomUser.objects.exclude(id=request.user.id)
    
    # Fetch active contacts
    contacts_qs = ContactRelation.objects.filter(Q(user1=request.user) | Q(user2=request.user), bloque=False)
    contact_users = []
    for c in contacts_qs:
        contact_users.append(c.user2 if c.user1 == request.user else c.user1)
        
    # Fetch all active discussions for the user
    discussions = Conversation.objects.filter(participants__user=request.user).distinct().order_by('-dateCreation')
    
    chat_list = []
    for d in discussions:
        if d.type_conv == 'prive':
            other_participant = d.participants.exclude(user=request.user).first()
            if other_participant:
                other_user = other_participant.user
                chat_list.append({
                    'id': d.id,
                    'type': d.type_conv,
                    'nom': f"{other_user.prenom} {other_user.nom}",
                    'photo': other_user.photoProfil.url if other_user.photoProfil else None,
                    'other_user_id': other_user.id
                })
        else:
            # Group chat
            try:
                groupe = d.groupe
                chat_list.append({
                    'id': d.id,
                    'type': d.type_conv,
                    'nom': groupe.nom,
                    'photo': groupe.photo.url if groupe.photo else None
                })
            except:
                pass

    return render(request, 'chat/index.html', {
        'users': users,
        'contacts': contact_users,
        'discussions': chat_list
    })


@login_required
def get_or_create_private_chat(request, user_id):
    if request.method == 'POST':
        try:
            other_user = CustomUser.objects.get(id=user_id)
            if request.user == other_user:
                return JsonResponse({'status': 'error', 'message': "Cannot chat with yourself"}, status=400)
                
            # Check if a private conversation already exists
            user_convs = Conversation.objects.filter(type_conv='prive', participants__user=request.user)
            existing_conv = user_convs.filter(participants__user=other_user).first()
            
            if existing_conv:
                return JsonResponse({'status': 'success', 'discussion_id': existing_conv.id})
                
            # Create a new conversation
            new_conv = Conversation.objects.create(type_conv='prive')
            Participant.objects.create(discussion=new_conv, user=request.user)
            Participant.objects.create(discussion=new_conv, user=other_user)
            
            return JsonResponse({'status': 'success', 'discussion_id': new_conv.id})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "User not found"}, status=404)
    return JsonResponse({'status': 'error', 'message': "Invalid method"}, status=405)

@login_required
def chat_room(request, discussion_id):
    try:
        discussion = Conversation.objects.get(id=discussion_id, participants__user=request.user)
        # We will render the room from index.html via JS fetching data, 
        # or we return a dedicated template if not single-page.
        # Since we are building an SPA-like interface with Vanilla JS, 
        # we can just return the chat data.
        
        messages = discussion.messages.order_by('dateEnvoi')
        msg_list = []
        for m in messages:
            msg_list.append({
                'id': m.id,
                'expediteur_id': m.expediteur.id,
                'expediteur_nom': m.expediteur.prenom,
                'contenu': m.contenu,
                'date': m.dateEnvoi.strftime('%H:%M'),
                'is_mine': m.expediteur.id == request.user.id
            })
            
        other_user = None
        if discussion.type_conv == 'prive':
            other_participant = discussion.participants.exclude(user=request.user).first()
            if other_participant:
                other_user = {
                    'nom': f"{other_participant.user.prenom} {other_participant.user.nom}",
                    'photo': other_participant.user.photoProfil.url if other_participant.user.photoProfil else None,
                    'en_ligne': other_participant.user.statutEnLigne
                }
                
        return JsonResponse({
            'status': 'success',
            'discussion_id': discussion.id,
            'messages': msg_list,
            'other_user': other_user
        })
    except Conversation.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': "Conversation not found"}, status=404)

@login_required
def create_group_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contact_ids = data.get('contact_ids', [])
            nom_groupe = data.get('nom', 'Nouveau Groupe')
            
            if not contact_ids:
                return JsonResponse({'status': 'error', 'message': "Sélectionnez au moins un contact."}, status=400)
                
            new_conv = Conversation.objects.create(type_conv='groupe')
            from .models import Groupe
            Groupe.objects.create(discussion=new_conv, nom=nom_groupe)
            
            Participant.objects.create(discussion=new_conv, user=request.user, role='admin')
            
            for cid in contact_ids:
                try:
                    target_user = CustomUser.objects.get(id=cid)
                    Participant.objects.create(discussion=new_conv, user=target_user)
                except CustomUser.DoesNotExist:
                    pass
            
            return JsonResponse({'status': 'success', 'discussion_id': new_conv.id})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': "Données invalides"}, status=400)
    return JsonResponse({'status': 'error', 'message': "Invalid method"}, status=405)
