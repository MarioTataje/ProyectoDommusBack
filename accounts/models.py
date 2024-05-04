from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from locations.models import District
from studies.models import Degree

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, blank=False, null=False)
    names = models.CharField(max_length=255, blank=False, null=False) 
    lastnames = models.CharField(max_length=255, blank=False, null=False)
    birth_date = models.DateTimeField(blank=False, null=False)
    genre = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    budget_min = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=6)
    budget_max = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=6)
    habits = models.CharField(max_length=255, blank=True, null=True)
    register_date = models.CharField(max_length=10, null=True)


    district = models.ForeignKey(District, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField('active', default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'



#    selfPersonality = models.ForeignKey( Personality, blank=False, on_delete=models.CASCADE )
#    targetPersonality = models.ForeignKey( Personality, blank=True, on_delete=models.CASCADE)
