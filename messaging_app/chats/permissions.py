from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """User can only access their own messages or conversations they participate in"""
    
    def has_object_permission(self, request, view, obj):
        # For messages
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        # For conversations
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        return False
