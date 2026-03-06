from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Statut
from accounts.models import ContactRelation
from django.db.models import Q
import json

@login_required
def get_status_feed(request):
    # Get active contacts
    contacts_qs = ContactRelation.objects.filter(Q(user1=request.user) | Q(user2=request.user), bloque=False)
    contact_users = [request.user] # include self
    for c in contacts_qs:
        contact_users.append(c.user2 if c.user1 == request.user else c.user1)
        
    now = timezone.now()
    active_statuses = Statut.objects.filter(user__in=contact_users, dateExpiration__gt=now).order_by('-datePublication')
    
    feed = []
    for s in active_statuses:
        feed.append({
            'id': s.id,
            'user_id': s.user.id,
            'user_nom': f"{s.user.prenom} {s.user.nom}",
            'user_photo': s.user.photoProfil.url if s.user.photoProfil else None,
            'type': s.typeStatut,
            'contenu': s.contenu,
            'date': s.datePublication.strftime('%H:%M')
        })
        
    return JsonResponse({'status': 'success', 'feed': feed})

@login_required
def add_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contenu = data.get('contenu', '')
            
            if not contenu.strip():
                return JsonResponse({'status': 'error', 'message': "Content cannot be empty"}, status=400)
                
            expiration = timezone.now() + timedelta(hours=24)
            
            Statut.objects.create(
                user=request.user,
                typeStatut='texte',
                contenu=contenu,
                dateExpiration=expiration
            )
            return JsonResponse({'status': 'success', 'message': "Statut ajouté"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': "Invalid method"}, status=405)
