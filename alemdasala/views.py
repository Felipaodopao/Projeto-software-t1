from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages 

# View para a página de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo(a), {username}!")
                # Redireciona para a home page ou para uma página de dashboard
                return redirect('home') # 'home' é o nome da URL para a sua página principal
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'alemdasala/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Você foi desconectado(a).")
    return redirect('login') # Redireciona para a página de login após o logout

def home_view(request):
     return render(request, 'alemdasala/home.html') 

def meditacao(request):
    return render(request, 'alemdasala/meditacao.html')