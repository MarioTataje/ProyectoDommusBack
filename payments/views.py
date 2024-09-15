from rest_framework.decorators import api_view
from rest_framework.views import *
from .serializers import PlanSerializer, UserPlanSerializer
from .models import Plan, UserPlan
from accounts.models import User
from .utils import update_user_plan

@api_view(['GET'])
def plans_list(request):
    if request.method == 'GET':
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def user_plan(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        user_plan = UserPlan.objects.get(user__id=user.id, active=True)
        serializer = UserPlanSerializer(user_plan)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            user_plan = update_user_plan(user, request.data)
        except Exception as e:
            return Response(str(e))
        serializer = UserPlanSerializer(user_plan)       
        return Response(serializer.data, status=status.HTTP_201_CREATED)
