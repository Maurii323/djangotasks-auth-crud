from django import forms
from .models import Task

class taskForm(forms.ModelForm):              # ModelForm sirve para crear un formulario en base a un modelo
    class Meta:
        model = Task                                    # se pone el modelo en el que se va a basar el form
        fields = ['title','description','important']    # se ponen los campos del modelo que va a pasarse por el form
        # se pone las clases css que va a tener cada campo
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control','placeholder':'write a title'}),
            'description' : forms.Textarea(attrs={'class':'form-control','placeholder':'write a description'}),
            'important' : forms.CheckboxInput(attrs={'class':'form-check-input'})
        }