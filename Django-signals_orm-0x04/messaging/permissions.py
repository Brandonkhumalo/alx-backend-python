from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants in a conversation.
    Applies to GET, POST, PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        # Only allow access to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        if isinstance(obj, Message):
            participants = obj.conversation.participants.all()
        elif isinstance(obj, Conversation):
            participants = obj.participants.all()
        else:
            return False

        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in participants

        return False
