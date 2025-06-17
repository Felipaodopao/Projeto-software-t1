from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login


def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "core/home.html", context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona para a home
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "core/login.html")

@login_required(login_url='login')
def home(request):
    return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'error': 'Usuário já existe.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Faz login automático após o cadastro
        return redirect('home')

    return render(request, 'core/register.html')

@login_required
def respiracao_view(request):
    return render(request, 'core/respiracao.html')