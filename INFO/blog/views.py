from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.urls import reverse
from django.views import generic
from .forms import UsuariosForm, LoginForm, ArticuloForm
from django.contrib.auth import login, logout, authenticate
from .models import Articulo
from django.core.paginator import Paginator

# from django.contrib.auth.forms import UserCreationForm

def index_view(request):
    context = {
        'is_index': True            # La variabla is_index es para un if en el html que cambia el header 
    }
    return render(request, 'index.html', context)

def blog(request):
    # Obtener todos los posts
    posts = Articulo.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj' : page_obj,   
    }
    
    return render(request, "blog/blog.html", context)

# class BlogView(generic.TemplateView):
#     template_name = "blog/base.html"


def post(request, post_id):                                # renderizar post
    post = get_object_or_404(Articulo, pk=post_id)
    return render(request, 'post.html', {'post': post})


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