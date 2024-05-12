from rest_framework import serializers
from .models import Match
from accounts.models import User
from accounts.serializers import UserSerializer


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
