from django.contrib import admin
from .models import Task
# lo que esta entre parentesis es lo que hereda
# esta clase sirve para personalizar el panel de Task
class TaskAdmin(admin.ModelAdmin):
    #indica cuales campos se muestran como solo lectura en la modificacion, tambien aparece sin poder rellenar en la creacion
    readonly_fields = ("created", )

# Register your models here.
admin.site.register(Task,TaskAdmin)