import datetime
import os
from math import log, log2

from django.urls import reverse
from django.utils import dateformat
from django.utils.timezone import now
from django.db import models
from django.db.models import Model, CharField, SlugField, IntegerField, FloatField
from django.core.files.storage import default_storage


def updateDb():
    words = Word.objects.all()
    for e in words:
        DCount = Document.objects.all().count()
        e.idf = log(DCount / e.count_from_docs)
        e.save()

class Word(Model):
    name = CharField(max_length=30, primary_key=True)
    count_from_docs = IntegerField()
    idf = FloatField(default=0)

    def __str__(self):
        return self.name

class Document(Model):
    name = CharField(max_length=30)
    slug = SlugField(
        allow_unicode=True
    )
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    words = models.ManyToManyField(Word, through='CountTable')


    def createSlug(self):
        self.slug = self.name + dateformat.format(now(), 'Y-m-d H:i:s')
        self.save()

    def analize(self, cleaned_info=None):
        f = default_storage.open(os.path.join(self.docfile.name), 'r')
        data = f.read()
        posible_elem = ["\n", ",",".","!","?",":"]
        for elem in posible_elem:
            data = data.replace(elem, " ")
        data = data.split(" ")
        datalist = dict.fromkeys(data, 0)
        for e in data:
            datalist[e] += 1
        if '' in datalist.keys():
            del datalist['']
        for key in datalist.keys():
            if Word.objects.filter(name=key).exists():
                word = Word.objects.filter(name=key)[0]
                word.count_from_docs+=1
            else:
                word = Word(name = key, count_from_docs = 1)
            DCount = Document.objects.all().count()
            word.idf = log(DCount / word.count_from_docs)
            word.save()
            m1 = CountTable(word=word, document=self,
                            count=datalist[key], idf = word.idf)
            m1.save()
            updateDb()

    def get_absolute_url(self):
        return reverse("getDoc", kwargs={
            'slug': self.slug
        })

class CountTable(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    count = models.IntegerField()
    idf = models.FloatField(default=0)
