from django.db import models
from .CustomValidations import *


class Personality(models.Model):
    idPersonality = models.AutoField(
        db_column='id_personality',
        primary_key=True
    )
    tag = models.CharField(
        db_column='tag',
        max_length=10,
        blank=False,
        null=False,
        validators=[validate_is_string]
    )
    mind = models.DecimalField(
        db_column='mind',
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=3
    )
    energy = models.DecimalField(
        db_column='energy',
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=3
    )
    nature = models.DecimalField(
        db_column='nature',
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=3
    )
    tactics = models.DecimalField(
        db_column='tactics',
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=3
    )
    identity = models.DecimalField(
        db_column='identity',
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=3
    )
    createdOn = models.DateTimeField(
        db_column='created_on',
        blank=False,
        null=False
    )
    status = models.BooleanField(
        db_column='status',
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'MAE_PERSONALITY'
