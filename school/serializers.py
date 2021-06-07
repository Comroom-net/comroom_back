from rest_framework import serializers

from .models import School, Comroom, AdminUser, Notice

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'