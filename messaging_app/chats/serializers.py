from rest_framework import serializers
from .models import User
from .models import Message
from .models import Conversation


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)


    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)


    class Meta:
        model = Conversation
        field = ['conversation_id', 'participants', 'messages', 'created_at']
