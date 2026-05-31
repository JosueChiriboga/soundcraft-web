from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Usuarios
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/editar/<int:pk>/', views.usuario_editar, name='usuario_editar'),
    path('usuarios/eliminar/<int:pk>/', views.usuario_eliminar, name='usuario_eliminar'),

    # Artistas
    path('artistas/', views.artista_list, name='artista_list'),

    # Canciones
    path('canciones/', views.cancion_list, name='cancion_list'),

    # Álbumes
    path('albumes/', views.album_list, name='album_list'),

    # Playlists
    path('playlists/', views.playlist_list, name='playlist_list'),

    # Reproducciones
    path('reproducciones/', views.reproduccion_list, name='reproduccion_list'),

    # Suscripciones
    path('suscripciones/', views.suscripcion_list, name='suscripcion_list'),

    # Pagos
    path('pagos/', views.pago_list, name='pago_list'),

    # Regalías
    path('regalias/', views.regalia_list, name='regalia_list'),

    # Reportes
    path('reportes/', views.reportes, name='reportes'),
]