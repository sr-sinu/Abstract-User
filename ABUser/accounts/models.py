from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class CustomUser(AbstractUser):
    dob = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    pic = models.FileField(blank=True, null=True)
    #email = models.EmailField(unique=True)
    #USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username


class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=100)
    question_desc = models.TextField()
    code_fld = models.TextField(default='')
    created_by = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    answersCount = models.IntegerField(default=0)


class Answers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=100)
    answer_desc = models.TextField(default='')
    code_fld = models.TextField(default='')
    answered_by = models.CharField(max_length=100)
    question_id = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    ans_count = models.IntegerField(default=0)
