from django import forms
from django.forms import ModelForm
from .models import Annotation, SNP

class SNPFilterForm(forms.Form):
    region = forms.CharField(
        label = 'Region',
        widget = forms.TextInput(attrs={'placeholder': 'chr1:500-1000', 'pattern': '^chr\d+:\d+-\d+$', 
                                      'class': 'form-control', 'style': 'max-width: 410px;'})
    )

    maf_min = forms.DecimalField(
        label = 'Min. value',
        widget = forms.NumberInput(attrs={'min': '0', 'max': '1', 'step': '0.01',
                                        'class': 'form-control', 'style': 'max-width: 100px;'})
    )
    maf_max = forms.DecimalField(
        label = 'Max. value',
        widget = forms.NumberInput(attrs={'min': '0', 'max': '1', 'step': '0.01',
                                        'class': 'form-control', 'style': 'max-width: 100px;'})
    )

class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = ['type', 'text']
        widgets = {
            'type' : forms.TextInput(attrs={'class' : 'form-control'}),
            'text' : forms.Textarea(attrs={'class' : 'form-control'}),
        }
        labels = {
            'type': 'Type',
            'text': 'Text',
        }
