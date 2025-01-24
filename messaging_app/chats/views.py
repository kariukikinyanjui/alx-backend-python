from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, Conversation, Message, ConversationParticipant
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']  # Only allow list and create

    def get_queryset(self):
        # Get conversations where the current user is a participant
        return self.request.user.conversations.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        # Add participants from request and current user
        participant_ids = request.data.get('participants', [])
        participant_ids.append(str(request.user.user_id))  # Ensure creator is included
        unique_ids = list(set(participant_ids))  # Remove duplicates

        # Create conversation participants
        for user_id in unique_ids:
            user = get_object_or_404(User, user_id=user_id)
            ConversationParticipant.objects.get_or_create(
                conversation=conversation,
                user=user
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']  # Only allow list and create

    def get_queryset(self):
        # Get messages for the conversation specified in URL
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(
            conversation__conversation_id=conversation_id
        ).order_by('sent_at')

    def perform_create(self, serializer):
        # Automatically set sender and conversation
        conversation = get_object_or_404(
            Conversation,
            conversation_id=self.kwargs['conversation_id']
        )
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )
