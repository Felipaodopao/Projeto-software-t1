from django.contrib import admin
from django.urls import path 
from alemdasala import views 
from django.urls import path, include
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs do app alem_da_sala diretamente aqui:
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'), 
    path("__reload__/", include("django_browser_reload.urls")),
]
