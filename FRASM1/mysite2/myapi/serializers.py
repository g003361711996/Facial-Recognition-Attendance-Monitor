# serializers.py
from rest_framework import serializers

from .models import Student

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('attributes','name', 'time_date', 'face_ids', 'image_link')