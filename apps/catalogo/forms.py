from django import forms
from .models import Cancha


class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = [
            'codigo', 'nombre', 'tipo', 'superficie', 'dimensiones',
            'descripcion', 'tarifa_bloque', 'cupos_bloques', 'estado',
            'imagen', 'destacado', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. F5T-03'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cancha F5 Techada 3'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'superficie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pasto sintético'}),
            'dimensiones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 25 x 15 m'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tarifa_bloque': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cupos_bloques': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Validar identificador único con clean_()
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '').strip().upper()
        existe = Cancha.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("Ya existe una cancha con este código.")
        return codigo

    # Valores cuantitativos no negativos
    def clean_tarifa_bloque(self):
        tarifa = self.cleaned_data.get('tarifa_bloque')
        if tarifa is not None and tarifa <= 0:
            raise forms.ValidationError("La tarifa debe ser superior a 0 CLP.")
        return tarifa
    