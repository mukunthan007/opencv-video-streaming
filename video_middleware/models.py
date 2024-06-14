from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class UploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file  = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.file_name
    
# class Fileid(models.Model):
#     #email = models.EmailField(default=None)
#     subfilename = models.CharField(max_length = 25, default=None)
#     fileid = models.ForeignKey(
#         "TrackFiles", on_delete=models.CASCADE
#     )

# class TrackFiles(models.Model):
#     email = models.EmailField(default=None)
#     file = models.CharField(max_length = 25 ,default=None)