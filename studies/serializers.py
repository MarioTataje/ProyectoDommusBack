from rest_framework import serializers
from .models import University, Degree


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('id', 'name')


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ('id', 'name')
