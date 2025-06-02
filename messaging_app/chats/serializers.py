from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # ✅ uses SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)  # ✅ uses CharField

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'sender_email',
            'message_body',
            'sent_at',
            'created_at'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True
    )
    messages = MessageSerializer(many=True, read_only=True, source='messages')
    title = serializers.CharField(write_only=True, required=False)  # ✅ uses CharField

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'messages', 'title']

    def validate_title(self, value):
        if 'badword' in value.lower():
            raise serializers.ValidationError("Title contains inappropriate content.")  # ✅ uses ValidationError
        return value

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participant_ids)
        return conversation
