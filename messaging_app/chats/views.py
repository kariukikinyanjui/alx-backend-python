from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Conversation
from .serializers import ConversationSerializer, ConversationCreateSerializer, MessageSerializer, MessageCreateSerializer
from rest_framework.generics import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.prefetch_related('participants', 'messages').all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['participants__user_id', 'created_at']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        serliazer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = seiralizer.save()
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('conversation', 'sender').all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['sender__user_id', 'send_at']
    ordering_fields = ['sent_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def list(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

