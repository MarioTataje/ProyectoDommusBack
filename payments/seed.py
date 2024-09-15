from payments.models import Plan

def create_data(apps, schema_editor):
    plans = ['Free', 'Pro']
    for p in plans:
        Plan(name=p).save()
