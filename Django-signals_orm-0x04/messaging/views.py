from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']  # latest messages first

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def get_queryset(self):
        return self.request.user.conversations.all().prefetch_related('participants', 'messages')

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if len(participant_ids) < 2:
            return Response({'detail': 'At least 2 participants are required.'}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() < 2:
            return Response({'detail': 'Invalid participants provided.'}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation', 'sender']
    ordering_fields = ['sent_at']
    ordering = ['sent_at']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user).select_related('sender', 'conversation')

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not sender_id or not message_body:
            return Response({'detail': 'conversation_id, sender_id, and message_body are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        if sender != request.user:
            return Response({'detail': 'You can only send messages as the authenticated user.'},
                            status=status.HTTP_403_FORBIDDEN)

        if sender not in conversation.participants.all():
            return Response({'detail': 'Sender is not a participant of the conversation.'},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        @login_required
        def delete_user(request):
            if request.method == "POST":
                user = request.user
                logout(request)
                user.delete()
                return redirect('home')

        @receiver(post_delete, sender=User)
        def delete_user_related_data(sender, instance, **kwargs):
            # Optional cleanup in case on_delete isn't used
            Message.objects.filter(sender=instance).delete()
            Message.objects.filter(receiver=instance).delete()
            Notification.objects.filter(user=instance).delete()
            MessageHistory.objects.filter(message__sender=instance).delete()
            MessageHistory.objects.filter(message__receiver=instance).delete()

        @login_required
        def send_message(request):
            if request.method == 'POST':
                form = MessageForm(request.POST)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.sender = request.user  # ✅ Correctly set the sender
                    message.save()
                    return redirect('inbox')  # Redirect to your inbox view
            else:
                form = MessageForm()
            return render(request, 'messaging/send_message.html', {'form': form})