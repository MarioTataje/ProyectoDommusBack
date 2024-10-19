from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from .serializers import UserSerializer, PersonalitySerializer, ContactSerializer
from .models import User, Contact
from locations.models import District
from studies.models import Degree, University

@api_view(['POST'])
def register_user(request):
    try:
        District.objects.get(id=request.data['district_id'])
    except District.DoesNotExist:
        raise Http404
    
    try:
        Degree.objects.get(id=request.data['degree_id'])
    except Degree.DoesNotExist:
        raise Http404
    
    try:
        University.objects.get(id=request.data['university_id'])
    except University.DoesNotExist:
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


@api_view(['POST'])
def verify_mail(request):
    if request.method == 'POST':
        email = request.data.get('email', None)
        if not email:
            return Response({'message': 'El campo email es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            return Response({'message': 'El email ya se encuentra asociado a un usuario'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Email disponible para utilizar'}, status=status.HTTP_200_OK)


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


@api_view(['GET', 'POST'])
def contacts_list(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        contacts = Contact.objects.filter(user__id=user_id)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



