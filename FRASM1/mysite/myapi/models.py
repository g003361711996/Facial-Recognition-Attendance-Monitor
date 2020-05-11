from django.db import models

class Student(models.Model):
    lecture_number = models.CharField(max_length=160)
    face_ids = models.CharField(max_length=160)
    def __str__(self):
        return self.face_ids
