from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as gl
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import re

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    location = 'London'
    description = models.CharField(max_length=200000)

    def __str__(self):
        return f'{self.title} in {self.company}'

class Resume(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    pdf_file = models.FileField(upload_to='resumes/', null=True, validators=[FileExtensionValidator(['pdf'])])
    text_content = models.TextField(blank=True)
