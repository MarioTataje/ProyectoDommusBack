from django.db import models
from .Personality import Personality
from .CustomValidations import *
from django.contrib.auth.hashers import make_password


class User(models.Model):
    idUser = models.AutoField(
        db_column='id_user',
        primary_key=True
    )
    selfPersonality = models.ForeignKey(
        Personality,
        db_column='id_self_personality',
        blank=False,
        related_name='self_personality',
        on_delete=models.CASCADE
    )
    targetPersonality = models.ForeignKey(
        Personality,
        db_column='id_target_personality',
        blank=True,
        related_name='target_personality',
        on_delete=models.CASCADE
    )
    names = models.CharField(
        db_column='names',
        max_length=255,
        blank=False,
        null=False,
        validators=[validate_is_string]
    )
    lastnames = models.CharField(
        db_column='lastnames',
        max_length=255,
        blank=False,
        null=False,
        validators=[validate_is_string]
    )
    genre = models.CharField(
        db_column='genre',
        max_length=50,
        blank=False,
        null=False,
        validators=[validate_is_string]
    )
    birthdate = models.DateTimeField(
        db_column='birthdate',
        blank=False,
        null=False,
        validators=[validate_born_date]
    )
    image = models.ImageField(
        db_column='image',
        upload_to='files/img/usuario',
        blank=True,
        null=True
        # default='core/img/prefil.png'
    )
    description = models.TextField(
        db_column='description',
        blank=True,
        null=True
    )
    email = models.EmailField(
        db_column='email',
        unique=True,
        blank=False,
        null=False
    )
    password = models.CharField(
        db_column='password',
        max_length=255,
        blank=False,
        null=False
    )
    degree = models.CharField(
        db_column='degree',
        max_length=255,
        blank=True,
        null=True
    )
    university = models.CharField(
        db_column='university',
        max_length=255,
        blank=True,
        null=True
    )
    budgetMin = models.DecimalField(
        db_column='budget_min',
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=3
    )
    budgetMax = models.DecimalField(
        db_column='budget_max',
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=3
    )
    district = models.CharField(
        db_column='district',
        max_length=255,
        blank=False,
        null=False
    )
    habits = models.CharField(
        db_column='habits',
        max_length=255,
        blank=True,
        null=True
    )
    lastLogin = models.DateTimeField(
        db_column='last_login',
        blank=True,
        null=True
    )
    status = models.BooleanField(
        db_column='status',
        blank=False,
        null=False
    )

    # @property
    # def get_imagenPerfil(self) -> str:
    #     if self.imagenPerfil and hasattr(self.imagenPerfil,'url'):
    #         return f'http://localhost:8000{self.imagenPerfil}'

    class Meta:
        db_table = 'MAE_USER'

    # def save(self, *args, **kwargs):
    #     self.contrasenia = make_password(self.contrasenia)
    #     super(Usuario, self).save(*args, **kwargs)
