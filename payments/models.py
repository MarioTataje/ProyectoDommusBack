from django.db import models
from accounts.models import User
from datetime import date

class Plan(models.Model):
    name = models.CharField(max_length=255)

    def str(self):
        return self.name

    class Meta:
        db_table = 'plans'


class UserPlan(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, related_name='user', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, blank=False, null=False, related_name='plan', on_delete=models.CASCADE)
    active = models.BooleanField(blank=False, null=False, default=True)
    amount = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    frequency = models.CharField(null=True, max_length=1)
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(null=True)

    @staticmethod
    def free_user(user):
        plan = Plan.objects.get(name='Free')
        user_plan = UserPlan(plan=plan, user=user, active=True, frequency='L', start_date=date.today())
        user_plan.save()
        return 

    class Meta:
        db_table = 'user_plans'
