from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum
from .models import (
    Usuario, Artista, Album, Cancion, Genero,
    Playlist, Reproduccion, Suscripcion, Pago,
    Regalia, UsuarioArtista, UsuarioCancion
)

# ============================================================
# DASHBOARD
# ============================================================
def dashboard(request):
    context = {
        'total_usuarios': Usuario.objects.count(),
        'total_artistas': Artista.objects.count(),
        'total_canciones': Cancion.objects.count(),
        'total_albumes': Album.objects.count(),
        'total_playlists': Playlist.objects.count(),
        'total_reproducciones': Reproduccion.objects.count(),
        'total_suscripciones': Suscripcion.objects.count(),
        'total_pagos': Pago.objects.count(),
        'ultimas_reproducciones': Reproduccion.objects.order_by('-fechaReproduccion')[:10],
        'top_canciones': Cancion.objects.annotate(
            total=Count('reproduccion')
        ).order_by('-total')[:5],
    }
    return render(request, 'dashboard.html', context)


# ============================================================
# USUARIOS
# ============================================================
def usuario_list(request):
    usuarios = Usuario.objects.all().order_by('idUsuario')
    return render(request, 'usuarios/list.html', {'usuarios': usuarios})

def usuario_crear(request):
    if request.method == 'POST':
        try:
            ultimo = Usuario.objects.order_by('-idUsuario').first()
            nuevo_id = (ultimo.idUsuario + 1) if ultimo else 1
            Usuario.objects.create(
                idUsuario=nuevo_id,
                nombreUsuario=request.POST['nombreUsuario'],
                apellidoUsuario=request.POST['apellidoUsuario'],
                correoUsuario=request.POST['correoUsuario'],
                contraseniaUsuario=request.POST['contraseniaUsuario'],
                fechaRegistroUsuario=request.POST['fechaRegistroUsuario'],
                paisUsuario=request.POST['paisUsuario'],
                tipoUsuario=request.POST['tipoUsuario'],
                estadoCuentaUsuario=request.POST['estadoCuentaUsuario'],
            )
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuario_list')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'usuarios/form.html', {'accion': 'Crear'})

def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, idUsuario=pk)
    if request.method == 'POST':
        try:
            usuario.nombreUsuario = request.POST['nombreUsuario']
            usuario.apellidoUsuario = request.POST['apellidoUsuario']
            usuario.correoUsuario = request.POST['correoUsuario']
            usuario.contraseniaUsuario = request.POST['contraseniaUsuario']
            usuario.fechaRegistroUsuario = request.POST['fechaRegistroUsuario']
            usuario.paisUsuario = request.POST['paisUsuario']
            usuario.tipoUsuario = request.POST['tipoUsuario']
            usuario.estadoCuentaUsuario = request.POST['estadoCuentaUsuario']
            usuario.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuario_list')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'usuarios/form.html', {'accion': 'Editar', 'usuario': usuario})

def usuario_eliminar(request, pk):
    usuario = get_object_or_404(Usuario, idUsuario=pk)
    if request.method == 'POST':
        try:
            usuario.delete()
            messages.success(request, 'Usuario eliminado exitosamente.')
            return redirect('usuario_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {e}')
    return render(request, 'usuarios/confirmar_eliminar.html', {'usuario': usuario})


# ============================================================
# ARTISTAS
# ============================================================
def artista_list(request):
    artistas = Artista.objects.select_related('Discografia_idDiscografia').order_by('idArtista')
    return render(request, 'artistas/list.html', {'artistas': artistas})


# ============================================================
# CANCIONES
# ============================================================
def cancion_list(request):
    canciones = Cancion.objects.select_related('Album_idAlbum').order_by('idCancion')
    return render(request, 'canciones/list.html', {'canciones': canciones})


# ============================================================
# ÁLBUMES
# ============================================================
def album_list(request):
    albumes = Album.objects.select_related('Artista_idArtista').order_by('idAlbum')
    return render(request, 'albumes/list.html', {'albumes': albumes})


# ============================================================
# PLAYLISTS
# ============================================================
def playlist_list(request):
    playlists = Playlist.objects.select_related('Usuario_idUsuario').order_by('idPlaylist')
    return render(request, 'playlists/list.html', {'playlists': playlists})


# ============================================================
# REPRODUCCIONES
# ============================================================
def reproduccion_list(request):
    reproducciones = Reproduccion.objects.select_related(
        'Usuario_idUsuario', 'Cancion_idCancion'
    ).order_by('-fechaReproduccion')
    return render(request, 'reproducciones/list.html', {'reproducciones': reproducciones})


# ============================================================
# SUSCRIPCIONES
# ============================================================
def suscripcion_list(request):
    suscripciones = Suscripcion.objects.select_related('Usuario_idUsuario').order_by('idSuscripcion')
    return render(request, 'suscripciones/list.html', {'suscripciones': suscripciones})


# ============================================================
# PAGOS
# ============================================================
def pago_list(request):
    pagos = Pago.objects.select_related('Suscripcion_idSuscripcion').order_by('idPago')
    return render(request, 'pagos/list.html', {'pagos': pagos})


# ============================================================
# REGALÍAS
# ============================================================
def regalia_list(request):
    regalias = Regalia.objects.select_related('Artista_idArtista').order_by('idRegalia')
    return render(request, 'regalias/list.html', {'regalias': regalias})


# ============================================================
# REPORTES
# ============================================================
def reportes(request):
    reproducciones_por_pais = (
        Reproduccion.objects
        .values('paisReproduccion')
        .annotate(total=Count('idReproduccion'))
        .order_by('-total')
    )
    top_canciones = (
        Cancion.objects
        .annotate(total=Count('reproduccion'))
        .order_by('-total')[:10]
    )
    ingresos_por_metodo = (
        Pago.objects
        .values('metodoPago')
        .annotate(total=Sum('montoPago'))
        .order_by('-total')
    )
    suscripciones_por_plan = (
        Suscripcion.objects
        .values('tipoPlanSuscripcion')
        .annotate(total=Count('idSuscripcion'))
        .order_by('-total')
    )
    context = {
        'reproducciones_por_pais': reproducciones_por_pais,
        'top_canciones': top_canciones,
        'ingresos_por_metodo': ingresos_por_metodo,
        'suscripciones_por_plan': suscripciones_por_plan,
    }
    return render(request, 'reportes/reportes.html', context)