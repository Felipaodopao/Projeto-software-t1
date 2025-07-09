from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages 
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date
from .models import Humor
from datetime import date, timedelta
from babel.dates import format_date
import locale
from .models import Tarefa, Consulta
from .models import Disponibilidade, Perfil
from django.shortcuts import render, redirect, get_object_or_404
from .models import Disponibilidade, Consulta

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "alemdasala/home.html", context)

def login_view(request):
    storage = messages.get_messages(request)
    list(storage)  # Consome todas as mensagens pendentes

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "alemdasala/login.html")


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
    data_param = request.GET.get('data')

    if isinstance(data_param, str):
        hoje = date.fromisoformat(data_param)
    else:
        hoje = date.today()

    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR')
        except:
            pass  
    
    

    data_formatada = format_date(hoje, format="full", locale='pt_BR').capitalize()

    humor_dia = Humor.objects.filter(usuario=request.user, data=hoje).first()

    inicio_semana = hoje - timedelta(days=hoje.weekday())
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    dados_semana = {}

    humor_map = {
        'feliz':    {'valor': 100, 'cor': '#ffe066', 'emoji': '😊'},
        'calmo':    {'valor': 80,  'cor': '#b2f2bb', 'emoji': '😌'},
        'ansioso':  {'valor': 40,  'cor': '#ffa94d', 'emoji': '😰'},
        'cansado':  {'valor': 30,  'cor': '#adb5bd', 'emoji': '😴'},
        'triste':   {'valor': 20,  'cor': '#74c0fc', 'emoji': '😢'},
        'irritado': {'valor': 10,  'cor': '#ff8787', 'emoji': '😠'},
        '':         {'valor': 5,   'cor': '#dee2e6', 'emoji': ''},
        None:       {'valor': 5,   'cor': '#dee2e6', 'emoji': ''},
    }

    for i in range(7):
        dia_data = inicio_semana + timedelta(days=i)
        entrada = Humor.objects.filter(usuario=request.user, data=dia_data).first()
        tipo = entrada.tipo if entrada else ''
        info = humor_map.get(tipo, humor_map[''])
        dados_semana[dias_semana[i]] = {
            'valor': info['valor'],
            'cor': info['cor'],
            'emoji': info['emoji'],
            'tipo': tipo,
        }

    contexto = {
    'data_hoje': hoje,  # pode usar se quiser em outros lugares
    'data_formatada': data_formatada,  # já vem pronta pro template
    'relato': humor_dia.relato if humor_dia else 'Nenhum registro encontrado.',
    'tipo_humor': humor_dia.tipo if humor_dia else '',
    'dados_semana': dados_semana,
}

    return render(request, 'alemdasala/historico.html', contexto)

@login_required(login_url='/register')
def meditacao(request):
    return render(request, 'alemdasala/meditacao.html')

@login_required(login_url='/register/')
def med_foco(request):
    return render(request, 'alemdasala/med_foco.html')

@login_required(login_url='/register/')
def med_relaxamento(request):
    return render(request, 'alemdasala/med_relaxamento.html')

@login_required(login_url='/register/')
def med_gratidao(request):
    return render(request, 'alemdasala/med_gratidao.html')

@login_required(login_url='/register/')
def med_estresse(request):
    return render(request, 'alemdasala/med_estresse.html')

@login_required(login_url='/register')
def organize_tempo(request):
    return render(request, "alemdasala/organiza.html") 

@login_required(login_url='/register')
def profissionais_view(request):
    return render(request, 'alemdasala/profissionais.html')

@login_required(login_url='/register')
def logsentimento(request):
    return render(request, 'alemdasala/logsentimento.html')

@login_required(login_url='/register')
def humor(request):
    if request.method == 'POST':
        tipo = request.POST.get('humor')
        relato = request.POST.get('descricao')
        data = timezone.now().date()
        usuario = request.user

        # Salva ou atualiza o humor do dia
        humor_obj, created = Humor.objects.update_or_create(
            usuario=usuario,
            data=data,
            defaults={'tipo': tipo, 'relato': relato}
        )
        messages.success(request, 'Humor registrado com sucesso!')
        return redirect('humor')  # Redireciona para a mesma página

    return render(request, 'alemdasala/humor.html')

@login_required(login_url='/register')
def psicologo(request):
    return render(request, 'alemdasala/psicologo.html')

@login_required(login_url='/register')
def psicopedagogo(request):
    return render(request, 'alemdasala/psicopedagogo.html')

@login_required(login_url='/register')
def organize_tempo(request):
    if request.method == 'POST':
        if 'add-task' in request.POST:
            descricao = request.POST.get('descricao')
            data = request.POST.get('data')
            if descricao and data:
                Tarefa.objects.create(usuario=request.user, descricao=descricao, data=data)
        elif 'concluir' in request.POST:
            tarefa_id = request.POST.get('concluir')
            Tarefa.objects.filter(id=tarefa_id, usuario=request.user).delete()

    tarefas = Tarefa.objects.filter(usuario=request.user).order_by('data')
    consultas = Consulta.objects.filter(usuario=request.user)
    return render(request, "alemdasala/organiza.html", {"tarefas": tarefas, "consultas": consultas})

@login_required(login_url='/register')
def psicologo(request):
    horarios = Disponibilidade.objects.filter(disponivel=True, profissional__perfil__tipo='psicologo')
    if request.method == "POST":
        horario_id = request.POST.get("horario_id")
        if horario_id:
            horario = Disponibilidade.objects.get(id=horario_id)
            horario.disponivel = False
            horario.save()
            Consulta.objects.create(
                usuario=request.user,
                data=horario.data,
                hora=horario.hora,  # <-- Adicione isto
                tipo="psicologo",
                observacao=f"Agendado com {horario.profissional.username}"
            )
            return redirect('psicologo')
        elif "delete_consulta" in request.POST:
            consulta_id = request.POST.get("delete_consulta")
            consulta = Consulta.objects.filter(id=consulta_id, usuario=request.user, tipo="psicologo").first()
            if consulta:
                # Extrai o username do campo observacao
                if consulta.observacao and "Agendado com " in consulta.observacao:
                    username = consulta.observacao.replace("Agendado com ", "").strip()
                else:
                    username = None
                disponibilidade = Disponibilidade.objects.filter(
                    profissional__perfil__tipo='psicologo',
                    profissional__username=username,
                    data=consulta.data
                ).first()
                if disponibilidade:
                    disponibilidade.disponivel = True
                    disponibilidade.save()
                consulta.delete()
    consultas = Consulta.objects.filter(usuario=request.user, tipo="psicologo")
    return render(request, 'alemdasala/psicologo.html', {"consultas": consultas, "horarios": horarios})

@login_required(login_url='/register')
def psicopedagogo(request):
    horarios = Disponibilidade.objects.filter(disponivel=True, profissional__perfil__tipo='psicopedagogo')
    if request.method == "POST":
        horario_id = request.POST.get("horario_id")
        if horario_id:
            horario = Disponibilidade.objects.get(id=horario_id)
            horario.disponivel = False
            horario.save()
            Consulta.objects.create(
                usuario=request.user,
                data=horario.data,
                hora=horario.hora,  # <-- Adicione isto
                tipo="psicologo",
                observacao=f"Agendado com {horario.profissional.username}"
            )
            return redirect('psicopedagogo')
        elif "delete_consulta" in request.POST:
            consulta_id = request.POST.get("delete_consulta")
            consulta = Consulta.objects.filter(id=consulta_id, usuario=request.user, tipo="psicopedagogo").first()
            if consulta:
                # Extrai o username do campo observacao
                if consulta.observacao and "Agendado com " in consulta.observacao:
                    username = consulta.observacao.replace("Agendado com ", "").strip()
                else:
                    username = None
                disponibilidade = Disponibilidade.objects.filter(
                    profissional__perfil__tipo='psicopedagogo',
                    profissional__username=username,
                    data=consulta.data
                ).first()
                if disponibilidade:
                    disponibilidade.disponivel = True
                    disponibilidade.save()
                consulta.delete()
    consultas = Consulta.objects.filter(usuario=request.user, tipo="psicopedagogo")
    return render(request, 'alemdasala/psicopedagogo.html', {"consultas": consultas, "horarios": horarios})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        list(messages.get_messages(request))
        return redirect('login')
    
@login_required
def agendar_consulta(request, tipo):
    horarios = Disponibilidade.objects.filter(disponivel=True)

    if request.method == 'POST':
        if 'delete_consulta' in request.POST:
            consulta_id = request.POST.get('delete_consulta')
            consulta = Consulta.objects.filter(id=consulta_id, usuario=request.user).first()
            if consulta:
                # Liberar o horário
                Disponibilidade.objects.filter(data=consulta.data, hora=consulta.hora, profissional__perfil__tipo=tipo).update(disponivel=True)
                consulta.delete()
            return redirect(request.path)

        horario_id = request.POST.get('horario_id')
        horario = Disponibilidade.objects.filter(id=horario_id, disponivel=True).first()
        if horario:
            horario.disponivel = False
            horario.save()
            Consulta.objects.create(
                usuario=request.user,
                data=horario.data,
                hora=horario.hora,
                tipo=tipo,
                observacao=f"Agendado com {horario.profissional.username}"
            )
            return redirect(request.path)

    consultas = Consulta.objects.filter(usuario=request.user, tipo=tipo)
    template = 'alemdasala/psicologo.html' if tipo == 'psicologo' else 'alemdasala/psicopedagogo.html'

    return render(request, template, {
        'horarios': horarios,
        'consultas': consultas,
    })
    

@login_required
def cadastrar_disponibilidade(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo == 'usuario':
        return redirect('home')

    if request.method == 'POST':
        if 'remover_horario' in request.POST:
            horario_id = request.POST.get('remover_horario')
            horario = Disponibilidade.objects.filter(id=horario_id, profissional=request.user, disponivel=True).first()
            if horario:
                horario.delete()
        else:
            data = request.POST.get('data')
            hora = request.POST.get('hora')
            if data and hora:
                Disponibilidade.objects.get_or_create(
                    profissional=request.user,
                    data=data,
                    hora=hora,
                    defaults={'disponivel': True}
                )

    disponibilidades = Disponibilidade.objects.filter(profissional=request.user)

    # buscar apenas consultas associadas ao profissional
    consultas = Consulta.objects.filter(
        data__in=[d.data for d in disponibilidades],
        tipo=request.user.perfil.tipo,
        observacao__icontains=request.user.username
    )

    ocupacoes = {
        f"{c.data}-{c.hora}": c.usuario.username
        for c in consultas
    }

    horarios_render = []
    for disp in disponibilidades:
        chave = f"{disp.data}-{disp.hora}"
        horarios_render.append({
            "id": disp.id,
            "data": disp.data,
            "hora": disp.hora,
            "disponivel": disp.disponivel,
            "ocupado_por": ocupacoes.get(chave)
        })

    return render(request, 'alemdasala/disponibilidade.html', {
        'horarios_render': horarios_render
    })



def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        tipo = request.POST.get('tipo', 'usuario')
        if User.objects.filter(username=username).exists():
            return render(request, 'alemdasala/register.html', {'error': 'Usuário já existe.'})
        user = User.objects.create_user(username=username, email=email, password=password)
        Perfil.objects.create(user=user, tipo=tipo)
        login(request, user)
        return redirect('home')
    return render(request, 'alemdasala/register.html')