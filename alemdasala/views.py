from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages 

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from datetime import date
from alemdasala.models import Humor
from datetime import timedelta

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "alemdasala/home.html", context)

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
    return render(request, "alemdasala/login.html")

# @login_required(login_url='login')

def home(request):
    return render(request, 'alemdasala/home.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'alemdasala/register.html', {'error': 'Usuário já existe.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Faz login automático após o cadastro
        return redirect('home')

    return render(request, 'alemdasala/register.html')

# @login_required
@login_required(login_url='/register')
def respiracao_view(request):
    return render(request, 'alemdasala/respiracao.html')


def historico_humor(request):
    data_hoje = request.GET.get('data') or date.today().isoformat()
    humor_dia = Humor.objects.filter(usuario=request.user, data=data_hoje).first()

    # Calcula o início da semana (segunda-feira)
    hoje = date.fromisoformat(data_hoje)
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    dados_semana = {}

    for i in range(7):
        dia_data = inicio_semana + timedelta(days=i)
        entrada = Humor.objects.filter(usuario=request.user, data=dia_data).first()
        dados_semana[dias_semana[i]] = int(entrada.nivel) if entrada else 0

    contexto = {
        'data_hoje': data_hoje,
        'data_formatada': humor_dia.data.strftime('%A, %d de %B') if humor_dia else '',
        'relato': humor_dia.relato if humor_dia else 'Nenhum registro encontrado.',
        'dados_semana': dados_semana
    }
    return render(request, 'alemdasala/historico.html', contexto)

@login_required(login_url='/register')
def meditacao(request):
    return render(request, 'alemdasala/meditacao.html')

@login_required(login_url='/register')
def organize_tempo(request):
    return render(request, "alemdasala/organiza.html") 

@login_required(login_url='/register')
def profissionais_view(request):
    return render(request, 'alemdasala/profissionais.html')