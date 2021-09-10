from django import forms

from .models import *

"""class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
    name = forms.CharField(
        label='Enter the name'
    )"""

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'docfile')