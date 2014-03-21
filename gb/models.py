from django.db import models
from mongoengine import *
from mongoengine.django.auth import User as MongoEngineUser
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage as s3_storage

class User(MongoEngineUser):

    #custom fields
    email = EmailField(verbose_name=_('e-mail address'),
                       unique=True)

class Document(models.Model):
    docfile = models.FileField(storage=s3_storage, upload_to='media')
