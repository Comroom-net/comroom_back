from rest_framework import serializers

from .models import Timetable, FixedTimetable


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = "__all__"


class FixedTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedTimetable
        fields = "__all__"
