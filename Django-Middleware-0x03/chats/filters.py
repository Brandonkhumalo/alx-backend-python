import django_filters
from .models import Message
from django.utils import timezone

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sender = django_filters.UUIDFilter(field_name='sender__user_id')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'start_date', 'end_date']