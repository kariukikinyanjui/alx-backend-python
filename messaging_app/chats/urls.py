from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework import routers


# Initialize the router and register the viewsets
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'conversations/<uuid:conversation_id>/messages/',
        MessageViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='conversation-messages'
    ),
]
