from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from django.views import View
from .models import Document


class List(View):
    def get(self, *args,**kwargs):
        docs = Document.objects.all()
        return render(self.request, 'Index.html', {'docs': docs})

class NewDoc(View):
    def get(self, *args, **kwargs):
        form = DocumentForm()
        return render(self.request, 'NewDoc.html', {'form': form})

    def post(self, *args, **kwargs):
        form = DocumentForm(self.request.POST, self.request.FILES)
        print(form)
        if form.is_valid():
            newdoc = form.save(commit=False)
            newdoc.createSlug()
            newdoc.save()
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('newDoc'))

