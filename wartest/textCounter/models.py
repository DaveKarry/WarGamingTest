import datetime

from django.db import models
from django.db.models import Model, CharField, SlugField


# Create your models here.


class Document(Model):
    name = CharField(max_length=30)
    slug = SlugField(
        allow_unicode=True
    )
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


    def createSlug(self):
        self.slug = self.name + str(self.docfile)
        self.save()