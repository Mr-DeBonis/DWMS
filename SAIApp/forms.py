from django import forms

from SAIApp.models import dwms_guia_header


class FormGuiaHeader(forms.ModelForm):
    class Meta:
        model = dwms_guia_header
        fields = ['folio']
        widgets = {
            'folio': forms.NumberInput(attrs={
                "placeholder":"Folio",
                "class":"form-control",
                "name": "folio",
                "required min": "1",
                "id": "id_folio",
                "required": "true"
            })
        }
        labels = {
            'folio': 'Folio:',
        }
