from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView

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
        if form.is_valid():
            newdoc = form.save(commit=False)
            newdoc.createSlug()
            newdoc.analize()
            newdoc.save()

            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('newDoc'))


class DocDetailView(ListView):
    template_name = "Document.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = self.document
        words = Word.objects.filter(document = self.document)
        context['words'] = words
        context['docCount'] = Document.objects.all().count()
        return context

    def get_queryset(self, **kwargs):
        self.document = get_object_or_404(Document, slug=self.kwargs['slug'])
        return CountTable.objects.filter(document=self.document).order_by('-idf')




