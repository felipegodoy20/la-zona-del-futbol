from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Perfil


def rut_valido(rut):
    """Valida el RUT chileno con el dígito verificador (módulo 11)."""
    rut = rut.replace('.', '').replace('-', '').upper()
    cuerpo, dv = rut[:-1], rut[-1:]
    if not cuerpo.isdigit() or len(cuerpo) < 7:
        return False
    suma, mult = 0, 2
    for d in reversed(cuerpo):
        suma += int(d) * mult
        mult = 2 if mult == 7 else mult + 1
    resto = 11 - (suma % 11)
    esperado = 'K' if resto == 10 else '0' if resto == 11 else str(resto)
    return dv == esperado


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="Nombres", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, label="Apellidos", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # Campos del perfil 
    rut = forms.CharField(max_length=12, required=True, label="RUT", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 12345678-5'}))
    telefono = forms.CharField(max_length=15, required=True, label="Teléfono", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. +56 9 1234 5678'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_rut(self):
        rut = self.cleaned_data.get('rut', '').replace('.', '').replace('-', '').upper()
        if not rut_valido(rut):
            raise forms.ValidationError("El RUT no es válido.")
        rut = f"{rut[:-1]}-{rut[-1]}"
        if Perfil.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Este RUT ya está registrado.")
        return rut

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Perfil.objects.create(
                usuario=user,
                rut=self.cleaned_data['rut'],
                telefono=self.cleaned_data['telefono'],
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    