from django.db import models
from .User import User


class Match(models.Model):
    idMatch = models.AutoField(
        db_column='id_match',
        primary_key=True
    )
    userSender = models.ForeignKey(
        User,
        db_column='id_user_sender',
        blank=False,
        null=False,
        related_name='user_sender',
        on_delete=models.CASCADE
    )
    userReciever = models.ForeignKey(
        User,
        db_column='id_user_reciever',
        blank=False,
        null=False,
        related_name='user_reciever',
        on_delete=models.CASCADE
    )
    flagMatch = models.BooleanField(
        db_column='flag_match',
        blank=False,
        null=False,
    )
    flagDismatch = models.BooleanField(
        db_column='flag_dismatch',
        blank=False,
        null=False,
    )
    status = models.BooleanField(
        db_column='status',
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'MAE_MATCH'
