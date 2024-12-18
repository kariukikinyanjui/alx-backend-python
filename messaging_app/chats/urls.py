from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet


router = DefaultRouter()
router.register(r'conversation', ConversationViewSet, basename='conversation')


message_list = MessageViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/<str:conversation_pk>/messages/', message_list, name='conversation-messages'),
]
