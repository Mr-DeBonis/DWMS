from django import forms

from SAIApp.models import dwms_guia_header, dwms_despacho, dwms_transporte, dwms_guia_desp, dwms_g_c_salida


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
                "required": "true",
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

        if transporte and transporte.nombre.strip().upper() == 'OTRO':
            if not otro_transporte:
                self.add_error('otro_transporte', 'Este campo es requerido cuando el transporte es OTRO.')
        else:
            cleaned_data['otro_transporte'] = ''

        return cleaned_data


class FormGuiaDespachada(forms.ModelForm):
    folio = forms.IntegerField(
        label='Folio',
        widget=forms.NumberInput(attrs={
            "placeholder": "Folio",
            "class": "form-control",
            "name": "folio",
            "min": "1",
            "id": "id_folio",
            "required": "true"
        })
    )

    class Meta:
        model = dwms_guia_desp
        fields = ['ot_transporte', 'nota', 'despacho']
        widgets = {
            'ot_transporte': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Orden de Transporte"
            }),
            'nota': forms.Textarea(attrs={
                'rows': 3,
                'autocorrect': 'on',
                'maxlength': 255,
                'style': 'resize:vertical',
                'class': 'form-control',
            }),
            'despacho': forms.HiddenInput(),
        }

    def clean_folio(self):
        folio = self.cleaned_data.get('folio')

        try:
            guia_header = dwms_guia_header.objects.get(folio=folio)
        except dwms_guia_header.DoesNotExist:
            raise forms.ValidationError("No hay una guía asociada a ese folio")

        if guia_header:
            if not dwms_g_c_salida.objects.filter(header=guia_header).exists():
                raise forms.ValidationError("El folio " + str(folio) + " no ha pasado por control de salida.")

        self.guia_header = guia_header
        return folio

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.guia_header = self.guia_header
        if commit:
            instance.save()
        return instance