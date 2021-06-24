from rest_framework import serializers

from .models import School, Comroom, AdminUser, Notice


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class ComroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comroom
        fields = "__all__"


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = "__all__"


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"
