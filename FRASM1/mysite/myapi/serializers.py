# serializers.py
from rest_framework import serializers

from .models import Student

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('lecture_number', 'face_ids')