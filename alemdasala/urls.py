from django.contrib import admin
from django.urls import path, include
from alemdasala import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meditacao/', views.meditacao, name='meditacao'),
    path('', views.home, name='home'),
    path('__reload__/', include('django_browser_reload.urls')),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('respiracao/', views.respiracao_view, name='respiracao'),
    path('historico/', views.historico_humor, name='historico'),
    path('organiza/', views.organize_tempo, name='organiza'),
    path('profissionais/', views.profissionais_view, name='profissionais'),

    # Outras rotas
    path('logsentino/', views.logsentimento, name='logsentimento'),
    path('humor/', views.humor, name='humor'),
    path('psicologo/', views.psicologo, name='psicologo'),
    path('psicopedagogo/', views.psicopedagogo, name='psicopedagogo'),

    # Meditações específicas
    path('meditacao/foco/', views.med_foco, name='med_foco'),
    path('meditacao/relaxamento/', views.med_relaxamento, name='med_relaxamento'),
    path('meditacao/gratidao/', views.med_gratidao, name='med_gratidao'),
    path('meditacao/estresse/', views.med_estresse, name='med_estresse'),
    path('logout/', views.logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)