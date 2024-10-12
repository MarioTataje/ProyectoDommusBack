from rest_framework import serializers
from .models import Plan, UserPlan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'name')


class UserPlanSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    start_date = serializers.SerializerMethodField('get_start_date')
    end_date = serializers.SerializerMethodField('get_end_date')

    def get_start_date(self, obj):
        return obj.start_date.strftime('%Y-%m-%d') if obj.start_date else None

    def get_end_date(self, obj):
        return obj.end_date.strftime('%Y-%m-%d') if obj.end_date else None

    class Meta:
        model = UserPlan
        fields = ('id', 'plan_name', 'frequency', 'amount', 'start_date', 'end_date')

