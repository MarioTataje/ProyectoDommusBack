from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from .serializers import MatchSerializer
from .models import Match
from accounts.models import User
from accounts.serializers import UserSerializer, PersonalitySerializer
from .utils import verify_like, verify_dislike, predict_ideal_personality, predict_ideal_roommates

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_matches(request, user_id):
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        matches = Match.objects.filter(sender_user__id=user_id, is_active=True)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_received_likes(request, user_id):
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        matches = Match.objects.filter(receiver_user__id=user_id, is_active=False)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_given_likes(request, user_id):
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        matches = Match.objects.filter(sender_user__id=user_id, is_active=False)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profiles(request, user_id):
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        sender_ids = Match.objects.filter(sender_user__id=user_id).values_list('receiver_user__id', flat=True)
        receiver_ids = Match.objects.filter(receiver_user__id=user_id, is_active=True).values_list('sender_user_id', flat=True)
        profiles = User.objects.exclude(id=user_id).exclude(id__in=sender_ids).exclude(id__in=receiver_ids)
  
        serializer = UserSerializer(profiles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ideal_personality(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        try:
            ideal_personality = predict_ideal_personality(user)
        except Exception as e:
            return Response({ 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PersonalitySerializer(ideal_personality)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ideal_rommates(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        try:
            ideal_personality = predict_ideal_personality(user)
            ideal_roommates = predict_ideal_roommates(ideal_personality)
        except Exception as e:
            return Response({ 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(ideal_roommates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
