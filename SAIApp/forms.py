from django import forms

from SAIApp.models import dwms_guia_header, dwms_despacho, dwms_transporte


class FormGuiaHeader(forms.ModelForm):
    class Meta:
        model = dwms_guia_header
        fields = ['folio']
        widgets = {
            'folio': forms.NumberInput(attrs={
                "placeholder": "Folio",
                "class": "form-control",
                "name": "folio",
                "required min": "1",
                "id": "id_folio",
                "required": "true"
            })
        }
        labels = {
            'folio': 'Folio:',
        }


class FormDespacho(forms.ModelForm):
    fecha_despacho = forms.DateTimeField(
        input_formats= ['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        })
    )

    class Meta:
        model = dwms_despacho
        fields = ['transporte', 'fecha_despacho', 'nota', 'otro_transporte']

        widgets = {
            'transporte': forms.Select(attrs={
                'class': 'form-control',
                'queryset': dwms_transporte.objects.filter(activo=True),
                'empty_label': None,
            }),
            'otro_transporte': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'nota': forms.Textarea(attrs={
                'rows': 3,
                'autocorrect': 'on',
                'maxlength': 255,
                'style': 'resize:vertical',
                'class': 'form-control',
            })
        }

    def __init__(self, *args, **kwargs):
        super(FormDespacho, self).__init__(*args, **kwargs)
        self.fields['transporte'].queryset = dwms_transporte.objects.filter(activo=True)
        self.fields['transporte'].empty_label = None

    def clean(self):
        cleaned_data = super(FormDespacho, self).clean()
        transporte = cleaned_data.get('transporte')
        otro_transporte = cleaned_data.get('otro_transporte')

        # Check if transporte is OTRO
        if transporte and transporte.nombre.strip().upper() == 'OTRO':
            if not otro_transporte:
                self.add_error('otro_transporte', 'Este campo es requerido cuando el transporte es OTRO.')
        else:
            # Clear the field if it's not OTRO
            cleaned_data['otro_transporte'] = ''

        return cleaned_data
