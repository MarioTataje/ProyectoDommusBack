from datetime import date

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from accounts.models import User, Personality, Contact
from locations.models import District
from studies.models import Degree, University

class PersonalitySerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["register_date"] = str(date.today())
        personality = Personality.objects.create(**validated_data)
        return personality

    class Meta:
        model = Personality

        fields = ('id', 'tag', 'mind', 'energy', 'nature', 'tactics', 'identity', 'register_date')
        read_only_fields = ('register_date',)


class UserSerializer(serializers.ModelSerializer):
    district_id = serializers.IntegerField(write_only=True)
    degree_id = serializers.IntegerField(write_only=True, required=False)
    university_id = serializers.IntegerField(write_only=True, required=False)
    district_name = serializers.CharField(source='district.name', read_only=True)
    degree_name = serializers.SerializerMethodField('get_degree_name')
    university_name = serializers.SerializerMethodField('get_university_name')
    personality = serializers.SerializerMethodField('get_personality')

    @staticmethod
    def validate_password(value: str) -> str:
        return make_password(value)

    def get_degree_name(self, instance):
        degree = instance.degree
        return degree.name if degree else None
    
    def get_university_name(self, instance):
        university = instance.university
        return university.name if university else None
    
    def get_personality(self, instance):
        personality = instance.self_personality
        return PersonalitySerializer(personality).data if personality else None

    def create(self, validated_data):
        district = District.objects.get(id=validated_data["district_id"])
        degree = Degree.objects.get(id=validated_data["degree_id"])
        university = Degree.objects.get(id=validated_data["university_id"])
        validated_data["district"] = district
        validated_data["degree"] = degree
        validated_data["university"] = university
        validated_data["register_date"] = str(date.today())
        user = User.objects.create(**validated_data)
        Contact.create_contact('Email', user.email, user)
        Contact.create_contact('WhatsApp', user.phone, user)
        return user
    
    def update(self, instance, validated_data):
        district_id = validated_data.pop('district_id', None)
        if district_id is not None:
            instance.district = District.objects.get(id=district_id)
        
        degree_id = validated_data.pop('degree_id', None)
        if degree_id is not None:
            instance.degree = Degree.objects.get(id=degree_id)

        university_id = validated_data.pop('university_id', None)
        if university_id is not None:
            instance.university = University.objects.get(id=university_id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'email', 'names', 'lastnames', 'password', 'birth_date', 'genre', 'description', 
                  'birth_date', 'budget_min', 'budget_max', 'phone', 'register_date', 'habits', 
                  'district_id', 'district_name', 'degree_id', 'degree_name', 'university_id', 
                  'university_name', 'personality')
        read_only_fields = ('register_date',)
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'type', 'description', 'status')
        read_only_fields = ('status',)