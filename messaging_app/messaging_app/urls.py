from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet
from rest_framework import routers
from chats import urls as chats_urls


router = routers.DefaultRouter()

router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(chats_urls)),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
