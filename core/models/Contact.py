from django.db import models
from .User import User


class Contact(models.Model):
    idContact = models.AutoField(
        db_column='id_contact',
        primary_key=True
    )
    user = models.ForeignKey(
        User,
        db_column='id_user',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        db_column='type',
        max_length=50,
        blank=False,
        null=False
    )
    description = models.CharField(
        db_column='description',
        max_length=255,
        blank=False,
        null=False
    )
    status = models.BooleanField(
        db_column='status',
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'MAE_CONTACT'
