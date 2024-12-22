from rest_framework.permissions import BasePermission


class IsParticipant(BasePermission):
    '''
    Custom permission to ensure the user is a participant of the conversationl
    '''
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        return request.user in obj.participants.all()
