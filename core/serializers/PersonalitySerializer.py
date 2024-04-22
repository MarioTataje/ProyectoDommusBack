from rest_framework import serializers
from core.models import Personality


class PersonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = '__all__'
