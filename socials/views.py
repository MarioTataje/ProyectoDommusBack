from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from .serializers import MatchSerializer
from .models import Match
from accounts.models import User
from .utils import verify_like, verify_dislike

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_like(request, sender_id, receiver_id):
    try:
        sender = User.objects.get(id=sender_id)
    except User.DoesNotExist:
        raise Http404
    
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        try:
            match = verify_like(sender, receiver)
        except Exception as e:
            return Response(str(e))
        serializer = MatchSerializer(match)        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_dislike(request, sender_id, receiver_id):
    try:
        sender = User.objects.get(id=sender_id)
    except User.DoesNotExist:
        raise Http404
    
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        try:
            match = verify_dislike(sender, receiver)
        except Exception as e:
            return Response(str(e))
        serializer = MatchSerializer(match)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
