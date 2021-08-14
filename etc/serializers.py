import logging

from rest_framework import serializers

from .models import Notice_nocookie
from school.models import Comroom

logger = logging.getLogger(__name__)


class NoticeNocookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice_nocookie
        fields = "__all__"
