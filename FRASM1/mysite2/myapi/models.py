from django.db import models


class Student(models.Model):
    attributes = models.TextField(max_length=1024)
    name = models.CharField(max_length=160)
    time_date = models.CharField(max_length=160)
    face_ids = models.CharField(max_length=160)
    image_link = models.CharField(max_length=160)
    def __str__(self):
        return self.face_ids
