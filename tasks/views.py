from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.forms import UserCreationForm  #Trae un formulario ya hecho para la registracion de usuarios
from django.contrib.auth.forms import AuthenticationForm #Trae un form para el login
from django.contrib.auth.models import User             #Trae el modulo de usuarios hecho por django
#sirve para crear una cookie con el token de la sesion del usuario para autorizar si esta logeado en posteriores paginas
from django.contrib.auth import login, logout, authenticate                
from django.db import IntegrityError                 #importa el error de intregridad para manejarlo en las excepciones
from .models import Task                            #importa los modelos creados manualmente
from .forms import taskForm                       #importa los formularios creados manualmente
from django.utils import timezone                  # modulo con las funciones de fechas
#valida si hay una sesion activa, si no la hay no deja ejecutar funciones que requieren un usuario logeado
#para poder redirigir al login, poner LOGIN_URL = 'url_login' en settings.py
from django.contrib.auth.decorators import login_required     

# funcion para registrarse
def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)    # Crea un usuario con la contraseña hasheada
                user.save()                                             # Guarda ese usuario creado en la base de datos
                login(request, user)                                    # Crea una cookie de sesión con el usuario autenticado 
                return redirect('home')
            except IntegrityError:          # maneja la excepcion de que el usuario ya existe en la base de datos
                return render(request,'signup.html',{             
                    'error' : 'Username already exists'
                })
        return render(request,'signup.html',{
            'error' : 'passwords do not match'
        })

#funcion para logearse con una cuenta ya creada
def signin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        #revisa si ese usuario existe y si la contraseña es correcta, devuelve el usuario si es valido, o vacio si no
        user = authenticate(request, username=username, password=password)
        if user is None:                            #si el usuario esta vacio
            return render(request,'login.html',{
            'error' : 'Username or password is incorrect'
            })
        else:
            login(request, user)                    #Crea una cookie de sesión con el usuario autenticado
            return redirect('home')

#funcion para deslogearse
@login_required                  #la funcion de abajo solamente va a poder ser ejecutada si existe una sesion activa
def signout(request):
    logout(request)        #elimina el cookie con la sesion activa del usuario
    return redirect('login')
       
# funcion para el home
def home(request):
    return render(request,'home.html',{
        'user' : request.user
    })

#funcion para crear una tarea
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'create_task.html',{
            'taskform' : taskForm
        })
    else:
        try:
            # crea y guarda la tarea con lo valores mandados en el formulario utilizando ese formulario que esta enlazado con el modelo task
            form = taskForm(request.POST)       # crea el formulario con los valores mandados en el POST
            new_task = form.save(commit=False)  # guarda los valores que estan dentro del formulario en new_task
            new_task.user = request.user        # guarda el usuario que creo esa tarea, el usuario de la sesion activa se guarda en la request
            new_task.save()                     # guarda la tarea creada en la base de datos
            return redirect('tasks')
        except ValueError:                      #maneja la excepcion de que hay un error en los valores enviados
            return render(request,'create_task.html',{
                'taskform' : taskForm,
                'error' : 'Please provide valid data'
            })

#funcion para mostrar las tareas
@login_required
def tasks(request):
    # consulta todas las tareas del usuario logeado que se guarda en request debido a la sesion activa
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = True) #devuelve las tareas sin completar
    return render(request,'tasks.html',{
        'tasks' : tasks
    })

#funcion para mostrar las tareas completadas
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = False) #devuelve las tareas completadas
    return render(request,'tasks_completed.html',{
        'tasks_completed' : tasks
    })

#funcion para mostrar el detalle de una tareas y poder modificar la tarea
@login_required
def task_details(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task,pk=task_id, user=request.user)  # busca una tarea por su id, que sea del usuario logeado
        form = taskForm(instance=task)              # crea un form, con el instance rellena los campos del form con el objeto que le pases
        return render(request,'task_details.html',{
            'task' : task,
            'taskform' : form
        })
    else:
        try:
            task = get_object_or_404(Task,pk=task_id, user=request.user)
            form = taskForm(request.POST,instance=task) #crea un form con todos los datos mandados por POST y basado en el objeto de task
            form.save()                                 #guarda los valores de ese form en la base de datos            
            return redirect('tasks')
        except ValueError:
            return render(request,'task_details.html',{
                'task' : task,
                'taskForm' : form,
                'error' : 'Error updating task'
            })

# funcion para marcar una tarea como completada
@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()            # timezone.now retorna la fecha en la que se ejecuta la funcion, asi se modifica un campo de esa task
        task.save()
        return redirect('tasks_completed')

#funcion para eliminar una tarea
@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()                               #elimina una tarea de la base de datos
        return redirect('tasks')




