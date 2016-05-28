from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import Coleccion


class CollectionForm(ModelForm):
    class Meta:
        model = Coleccion
        fields = ['nombre', 'descripcion', 'media']

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['descripcion'].required = True
        self.fields['media'].required = True


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
