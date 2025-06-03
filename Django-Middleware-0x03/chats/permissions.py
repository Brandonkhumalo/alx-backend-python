from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants in a conversation.
    """

    def has_permission(self, request, view):
        # Require the user to be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Message objects
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        # For Conversation objects
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        return False
