from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)


    class Meta:
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender', 
            'conversation',
            'message_body',
            'sent_at'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializers(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)


    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at'
        ]
