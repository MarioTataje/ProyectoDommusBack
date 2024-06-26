from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from locations.models import District
from studies.models import Degree, University
from .managers import UserManager
from datetime import date


class Personality(models.Model):
    tag = models.CharField(max_length=10, blank=False, null=False)
    mind = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=3)
    energy = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=3)
    nature = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=3)
    tactics = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=3)
    identity = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=3)
    register_date = models.DateField(blank=False, null=False)
    is_active = models.BooleanField('active', blank=False, null=False, default=True)

    def get_personality_profile(self):
        personality_profile = [self.energy, self.mind, self.nature, self.tactics, self.identity]
        return personality_profile
    
    @staticmethod
    def get_ideal_personality(ideal_list):
        personality = Personality(id=0, tag='Personalidad ideal', energy= ideal_list[0], mind=ideal_list[1], 
                                  nature=ideal_list[2], tactics=ideal_list[3], identity=ideal_list[4], 
                                  register_date=date.today())
        return personality
    
    class Meta:
        db_table = 'personalities'


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, blank=False, null=False)
    names = models.CharField(max_length=255, blank=False, null=False) 
    lastnames = models.CharField(max_length=255, blank=False, null=False)
    birth_date = models.DateTimeField(blank=False, null=False)
    genre = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    budget_min = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=6)
    budget_max = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=6)
    habits = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=False, null=False)
    register_date = models.CharField(max_length=10, null=True)

    district = models.ForeignKey(District, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, blank=True, null=True, on_delete=models.CASCADE)
    university = models.ForeignKey(University, blank=True, null=True, on_delete=models.CASCADE)
    self_personality = models.ForeignKey(Personality, related_name='self_personality', blank=True, 
                                        null=True, on_delete=models.CASCADE)
    target_personality = models.ForeignKey(Personality, related_name='target_personality', blank=True, 
                                        null=True, on_delete=models.CASCADE)

    is_active = models.BooleanField('active', default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class Contact(models.Model):

    type = models.CharField(max_length=50, blank=False, null=False) 
    description = models.CharField(max_length=255, blank=False, null=False)
    status = models.BooleanField('status', blank=True, default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def create_contact(contact_type, description, user):
        contact = Contact(type=contact_type, description=description, status=True, user=user)
        contact.save()
        return 

    class Meta:
        db_table = 'contacts'

