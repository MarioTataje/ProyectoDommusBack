from django.db import models
from accounts.models import User

class Match(models.Model):
    sender_user = models.ForeignKey(User, blank=False, null=False, related_name='sender_user', on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(User, blank=False, null=False, related_name='receiver_user', on_delete=models.CASCADE)
    flag_match = models.BooleanField(blank=False, null=False)
    flag_dismatch = models.BooleanField(blank=False, null=False)
    is_active = models.BooleanField('active', blank=False, null=False, default=True)
    class Meta:
        db_table = 'matchs'
