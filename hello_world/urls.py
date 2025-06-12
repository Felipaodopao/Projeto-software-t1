from django.contrib import admin
from django.urls import path # Não precisa de 'include' se não houver urls.py nos apps
from alemdasala import views # Importe as views do seu app alemdasala

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs do app alem_da_sala diretamente aqui:
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'), # A URL da sua página inicial
    # Se você tiver outras views em alemdasala, adicione-as aqui
]