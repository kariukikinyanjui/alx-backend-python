from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet


router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


urlpatterns = [
    path('', include(router.urls)),
    path('conversations/<str:conversation_pk>/messages/', message_list, name='conversation-messages'),
]
