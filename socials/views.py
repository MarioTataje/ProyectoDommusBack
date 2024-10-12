from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *
from django.db.models import Q
from decimal import Decimal

from .serializers import MatchSerializer, ReportSerializer
from .models import Match, Report
from accounts.models import User
from payments.models import UserPlan
from accounts.serializers import UserSerializer, PersonalitySerializer
from .utils import verify_like, verify_dislike, predict_ideal_personality, predict_ideal_roommates, filtrar_ideal_roommates

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
            user_plan = UserPlan.objects.get(user=sender, active=True)
            if user_plan and user_plan.frequency == 'L':
                like_count = Match.objects.filter(sender_user=sender, is_active=True).count()
                if like_count >= 15:
                    return Response({'error': 'Has alcanzado el límite de 15 likes por día.'}, status=status.HTTP_400_BAD_REQUEST)
            
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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_match(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        raise Http404
    
    if request.method == 'DELETE':
        match.is_active = None
        match.save()
        return Response({'message': 'Match eliminado'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_matches(request, user_id):
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        matches = Match.objects.filter(
            (Q(sender_user__id=user_id) | Q(receiver_user__id=user_id)) & Q(is_active=True)
        )
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
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        sender_ids = Match.objects.filter(sender_user__id=user_id).values_list('receiver_user__id', flat=True)
        receiver_ids = Match.objects.filter(receiver_user__id=user_id, is_active=True).values_list('sender_user_id', flat=True)
        try:
            budget_min = user.budget_min - Decimal('300.0')
            budget_max = user.budget_max + Decimal('300.0')
            district_id = user.district.id 
            profiles = User.objects.exclude(id=user_id).exclude(id__in=sender_ids).exclude(id__in=receiver_ids)
            profiles = profiles.filter(budget_min__gte=budget_min, budget_max__lte=budget_max, district__id=district_id)

            user_plan = UserPlan.objects.get(user=user, active=True)
            if user_plan and user_plan.frequency == 'L':
                profiles = profiles[:15]

        except Exception as e:
            return Response(str(e))
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_ideal_rommates(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        try:
            ideal_personality = predict_ideal_personality(user)
            ideal_roommates = predict_ideal_roommates(ideal_personality)
            if request.data and bool(request.data):
                filtrar_ideal_roommates(request.data)
        except Exception as e:
            return Response({ 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(ideal_roommates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_user(request, reporting_id, reported_id):
    try:
        reporting_user = User.objects.get(pk=reporting_id)
    except User.DoesNotExist:
        raise Http404
    
    try:
        reported_user = User.objects.get(pk=reported_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporting_user, reported_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reports_by_reporting(request, reporting_id):
    try:
        User.objects.get(pk=reporting_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        reports = Report.objects.filter(reporting_user__id=reporting_id)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reports_by_reported(request, reported_id):
    try:
        User.objects.get(pk=reported_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        reports = Report.objects.filter(reporting_user__id=reported_id)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
