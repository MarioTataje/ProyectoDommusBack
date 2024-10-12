from .models import Plan, UserPlan
from datetime import date
from dateutil.relativedelta import relativedelta

def update_user_plan(user, data):
    cancel_plan(user)
    frequency = data.get('frequency', None)
    amount = data.get('amount', None)
    
    frequency_map = {
        'L': ('Free', None),
        'M': ('Pro', relativedelta(months=1)),
        'T': ('Pro', relativedelta(months=3))
    }

    plan_name, end_date_delta = frequency_map.get(frequency, ('Free', None))

    plan = Plan.objects.get(name=plan_name)
    start_date = date.today()
    end_date = start_date + end_date_delta if end_date_delta else None

    user_plan = UserPlan.objects.create(
        user=user,
        plan=plan,
        amount=amount,
        frequency=frequency,
        start_date=start_date,
        end_date=end_date
    )

    return user_plan


def cancel_plan(user):
    previous_plan = UserPlan.objects.get(user__id=user.id, active=True)
    previous_plan.active = False
    previous_plan.end_date = date.today() if previous_plan.frequency else None
    previous_plan.save()
