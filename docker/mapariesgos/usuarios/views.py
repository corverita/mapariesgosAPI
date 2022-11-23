from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import UserForm

# Create your views here.

class Registro(CreateView):
    model = User
    form_class: UserCreationForm
    template_name = "registro.html"
    success_url = reverse_lazy('login')
    
class LoginUsuario(LoginView):
    model = User
    template_name = 'login.html'
    success_url = reverse_lazy('web:home')
    
class LogoutUsuario(LogoutView):
    pass

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            messages.add_message(request, messages.INFO, f'Bienvenido {user.get_username()}')
            return redirect('web:home')
        else:
            messages.add_message(request, messages.ERROR, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')
