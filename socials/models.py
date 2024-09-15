from django.db import models
from accounts.models import User

class Match(models.Model):
    sender_user = models.ForeignKey(User, blank=False, null=False, related_name='sender_user', on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(User, blank=False, null=False, related_name='receiver_user', on_delete=models.CASCADE)
    flag_match = models.BooleanField(blank=True, null=True)
    flag_dismatch = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField('active', blank=True, null=True, default=False)
    register_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'matches'


class Report(models.Model):
    reporting_user = models.ForeignKey(User, blank=False, null=False, related_name='reporting_user', on_delete=models.CASCADE)
    reported_user = models.ForeignKey(User, blank=False, null=False, related_name='reported_user', on_delete=models.CASCADE)
    times_reported = models.IntegerField(blank=False, null=False)
    reason = models.CharField(max_length=255, null=False)
    description =  models.TextField(blank=False, null=False)
    register_date = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'reports'
