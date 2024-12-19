from rest_framework import serializers
from .models import User
from .models import Message
from .models import Conversation


class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)


    class Meta:
        model = User
        field = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()


    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    def get_sender(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializers(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()


    class Meta:
        model = Conversation
        field = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_participant_count(self, obj):
        return obj.participant.count()

    def validate(self, data):
        if 'participants' in data and len(data['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data
