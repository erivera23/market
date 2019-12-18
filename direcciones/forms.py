from django.forms import ModelForm
from .models import Direccion

class DireccionForm(ModelForm):
    class Meta:
        model = Direccion
        fields = [
            'line1', 'line2', 'ciudad', 'estado', 'pais', 'codigo_postal', 'referencia'
        ]

        labels = {
            'line1': 'Calle 1',
            'line2': 'Calle 2',
            'ciudad': 'Ciudad',
            'estado': 'Estado',
            'pais': 'País',
            'codigo_postal': 'Código postal',
            'referencia': 'Referencias'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['line1'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['line2'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['ciudad'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['estado'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['pais'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['codigo_postal'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '0000'
        })

        self.fields['referencia'].widget.attrs.update({
            'class': 'form-control'
        })