import logging

from rest_framework import serializers

from .models import Timetable, FixedTimetable
from school.models import Comroom

logger = logging.getLogger(__name__)


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = "__all__"


class FixedTimetableSerializer(serializers.ModelSerializer):
    comroom = serializers.StringRelatedField(read_only=True)
    comroom_id = serializers.PrimaryKeyRelatedField(
        queryset=Comroom.objects.all(), write_only=True, source="comroom"
    )

    class Meta:
        model = FixedTimetable
        fields = "__all__"
