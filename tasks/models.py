from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # determina si el campo es requerido en un formulario,si no se pasa una descripcion el campo va a ser vacio
    created = models.DateTimeField(auto_now_add=True) # se autocompleta con la fecha y hora que se creo la tarea
    datecompleted = models.DateTimeField(null=True,blank=True)  # indica que este campo va a ser vacio inicialmente
    important = models.BooleanField(default=False)  # por defecto el valor es falso
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # cuando se elimine un usuario, se eliminan todas sus tareas

    # metodo para que en el panel de administracion apareza representado con su title y el nombre del usuario relacionado
    def __str__(self):
        return f'{self.title}-{self.user.username}'