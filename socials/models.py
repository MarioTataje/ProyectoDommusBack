from django.db import models
from accounts.models import User

class Match(models.Model):
    sender_user = models.ForeignKey(User, blank=False, null=False, related_name='sender_user', on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(User, blank=False, null=False, related_name='receiver_user', on_delete=models.CASCADE)
    flag_match = models.BooleanField(blank=True, null=True)
    flag_dismatch = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField('active', blank=True, null=True, default=False)
    class Meta:
        db_table = 'matches'
