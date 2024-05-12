from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from .serializers import UserSerializer, PersonalitySerializer
from .models import User, Personality
from locations.models import District

@api_view(['POST'])
def register_user(request):
    try:
        District.objects.get(id=request.data['district_id'])
    except District.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def self_personality_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        personality = user.self_personality    
        serializer = PersonalitySerializer(personality)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PersonalitySerializer(data=request.data)
        if serializer.is_valid():
            personality = serializer.save()
            user.self_personality = personality
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET', 'POST'])
def target_personality_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        personality = user.target_personality    
        serializer = PersonalitySerializer(personality)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PersonalitySerializer(data=request.data)
        if serializer.is_valid():
            personality = serializer.save()
            user.target_personality = personality
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
