from datetime import date
from rest_framework import serializers
from .models import Match, Report
from accounts.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist


class MatchSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField('get_sender', read_only=True)
    receiver = serializers.SerializerMethodField('get_receiver', read_only=True)

    @staticmethod
    def get_sender(self):
        sender = self.sender_user
        return UserSerializer(sender).data
    
    @staticmethod
    def get_receiver(self):
        receiver = self.receiver_user
        return UserSerializer(receiver).data

    class Meta:
        model = Match
        fields = ('id', 'flag_match', 'flag_dismatch', 'sender', 'receiver', 'is_active')
        read_only_fields = ('is_active', 'flag_match', 'flag_dismatch')

class ReportSerializer(serializers.ModelSerializer):
    reporting = serializers.SerializerMethodField('get_reporting', read_only=True)
    reported = serializers.SerializerMethodField('get_reported', read_only=True)

    @staticmethod
    def get_reporting(self):
        reporting = self.reporting_user
        return UserSerializer(reporting).data
    
    @staticmethod
    def get_reported(self):
        reported = self.reported_user
        return UserSerializer(reported).data
    
    
    def create(self, validated_data):
        reporting_user = validated_data["reporting_user"]
        reported_user = validated_data["reported_user"]
        report = None        
        try:
            report = Report.objects.get(reporting_user=reporting_user, reported_user=reported_user)
            report.times_reported += 1
            report.save()
        except ObjectDoesNotExist:
            validated_data["times_reported"] = 1
            validated_data["register_date"] = str(date.today())
            report = Report.objects.create(**validated_data)
        return report
    
    class Meta:

        model = Report
        fields = ('id', 'times_reported', 'reason', 'description', 'register_date', 'reporting', 'reported')
        read_only_fields = ('times_reported', 'register_date', )
