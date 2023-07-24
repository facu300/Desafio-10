from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.urls import reverse
from django.views import generic
from .forms import UsuariosForm, LoginForm, ArticuloForm, ComentarioForm
from django.contrib.auth import login, logout, authenticate
from .models import Articulo, Comentario, Usuarios
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.models import User
from .forms import PermisosUsuarioForm

def index_view(request):
    context = {
        'is_index': True            # La variabla is_index es para un if en el html que cambia el header 
    }
    return render(request, 'index.html', context)

def blog(request):
    # Obtener todos los posts
    posts = Articulo.objects.all()

    # Obtener los últimos 6 artículos ordenados por fecha de creación
    ultimos_post = Articulo.objects.filter(publicado=True).order_by('-creacion')[:6]

    context = {
        'posts': posts,
        'ultimos_post': ultimos_post
    }
    return render(request, "blog/blog.html", context)

# class BlogView(generic.TemplateView):
#     template_name = "blog/base.html"


# def post(request, post_id):                                # renderizar post
#     post = get_object_or_404(Articulo, pk=post_id)
#     return render(request, 'post.html', {'post': post})

def post(request, post_id):
    post = get_object_or_404(Articulo, pk=post_id)

    # Obtener los últimos 6 artículos ordenados por fecha de creación
    ultimos_post = Articulo.objects.filter(publicado=True).exclude(id=post_id).order_by('-creacion')[:6]
    
    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario', '')
        if comentario_texto.strip():  # Asegurarse de que el comentario no esté en blanco
            comentario = Comentario(
                id_articulo=post,
                id_usuario=request.user,
                contenido=comentario_texto,
                
            )
            comentario.save()
    
    comentarios = Comentario.objects.filter(id_articulo=post_id)
    
    return render(request, 'post.html', {'post': post, 'comentarios': comentarios, 'ultimos_post': ultimos_post})


def register_view(request):
    
    if request.method == 'POST':
        form = UsuariosForm(request.POST)     # Procesa el formulario si se envió una solicitud POST
        
        if form.is_valid():

            user = form.save()                 # Almacena el usuario en la db

            if user is not None:
                login(request, user)           # Se loguea el usuario recién creado
                return redirect("blog:index")  # Se redirecciona al index
        
    else:
        form = UsuariosForm()
        print(form.errors)            # Si el formulario no es válido, se mostrará con los mensajes de error
    return render(request, 'register.html', {'form': form})

def login_view(request):                      # view que gestiona el login
    
    if not request.user.is_anonymous:   # Si el usuario ya está logueado vuelve al index sin entrar a la vista
        return redirect('blog:index')


    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Si el login fue exitoso, redirige al usuario al index.
                return redirect('blog:index')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('blog:index')


def new_post_view(request):
    if request.user.is_anonymous:
        return redirect('blog:index')

    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.autor = request.user
            form.save()
            print('ingresó acá')
            
            return redirect('blog:post', post_id=article.id)
    else:
        form = ArticuloForm()

    return render(request, 'new_post.html', {'form': form})


def delete_comment(request, comentario_id):
    if request.method == "POST":
        comentario = get_object_or_404(Comentario, pk=comentario_id)
        if comentario.id_usuario == request.user:
            comentario.delete()
    return redirect('blog:post', post_id=comentario.id_articulo.id)


# ----------------------------------- Edición de Permisos -----------------------

def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin, login_url='/')
def edit_users_permissions(request):
    if request.method == 'POST':
        for user in Usuarios.objects.all():
            is_staff = request.POST.get('is_staff_{}'.format(user.id)) == 'on'
            es_colaborador = request.POST.get('es_colaborador_{}'.format(user.id)) == 'on'
            user.is_staff = is_staff
            user.es_colaborador = es_colaborador
            user.save()

    users = Usuarios.objects.all()
    form = PermisosUsuarioForm()

    return render(request, 'permissions.html', {'users': users, 'form': form})

# ------------------------------------ Edición de posts

def editar_post(request, post_id):
    post = get_object_or_404(Articulo, pk=post_id)

    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post', post_id=post.id)
    else:
        form = ArticuloForm(instance=post)

    return render(request, 'editar_post.html', {'form': form})



def eliminar_post(request, post_id, confirmacion=False):
    post = get_object_or_404(Articulo, pk=post_id)

    if confirmacion:
        post.delete()
        return redirect('blog:blog')

    return render(request, 'eliminar_post.html', {'post': post})