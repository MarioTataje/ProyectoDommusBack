from datetime import date

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from accounts.models import User
from locations.models import District


class UserSerializer(serializers.ModelSerializer):
    district_id = serializers.IntegerField(write_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    @staticmethod
    def validate_password(value: str) -> str:
        return make_password(value)

    def create(self, validated_data):
        district = District.objects.get(id=validated_data["district_id"])
        validated_data["district"] = district
        validated_data["register_date"] = str(date.today())
        user = User.objects.create(**validated_data)
        return user


    class Meta:
        model = User
        fields = ('id', 'email', 'names', 'lastnames', 'password', 'birth_date', 'genre', 'description', 
                  'birth_date', 'budget_min', 'budget_max', 'register_date', 'habits', 
                  'district_id', 'district_name')
        read_only_fields = ('register_date',)
        extra_kwargs = {
            'password': {'write_only': True},
        }
