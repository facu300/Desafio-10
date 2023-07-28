from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.urls import reverse
from django.views import generic
from .forms import UsuariosForm, LoginForm, ArticuloForm, ComentarioForm, ModificarUsuarioForm, CategoriaCrearEditarForm, EtiquetaForm, FormContacto
from django.contrib.auth import login, logout, authenticate
from .models import Articulo, Comentario, Usuarios, Categoria, Etiqueta, Categoria_Articulo
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.models import User
from .forms import PermisosUsuarioForm
from django.core.paginator import Paginator
from django.db.models import Q

def index_view(request):
    
    if request.method == 'POST':
        form = FormContacto(request.POST)
        if form.is_valid():
            form.save()  # Guarda el mensaje en la base de datos si el formulario es válido
            # Aquí puedes agregar lógica adicional si es necesario, como enviar un correo electrónico, etc.
    else:
        form = FormContacto()
    
    context = {
        'is_index': True,          # La variable is_index es para un if en el html que cambia el header 
        'form': form
    }
    return render(request, 'index.html', context)

def blog(request):
    nombre = request.GET.get('categoria', None)
    tags_nombre = request.GET.get('tags', None)
    print(tags_nombre)

    if nombre is not None:
        posts = Articulo.objects.filter(categoria__nombre=nombre).order_by('-creacion')[:6]

        categorias = Categoria.objects.all()
        # Obtengo los últimos 6 artículos ordenados por fecha de creación
        ultimos_post = Articulo.objects.filter(publicado=True).order_by('-creacion')[:6]

        # Obtengo todas las etiquetas
        etiquetas = Etiqueta.objects.all()

        # renderizo 4 post por página
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'posts': posts,
            'categorias': categorias,
            'ultimos_post': ultimos_post,
            'etiquetas': etiquetas,
            'page_obj': page_obj,
        }
        return render(request, "blog/blog.html", context)
    
    elif tags_nombre is not None:
        print('entro acá')

        posts = Articulo.objects.filter(etiqueta__nombre=tags_nombre).order_by('-creacion')[:6]
        categorias = Categoria.objects.all()
        # Obtengo los últimos 6 artículos ordenados por fecha de creación
        ultimos_post = Articulo.objects.filter(publicado=True).order_by('-creacion')[:6]

        etiquetas = Etiqueta.objects.all()

        # renderizo 4 post por página
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'posts': posts,
            'categorias': categorias,
            'ultimos_post': ultimos_post,
            'etiquetas': etiquetas,
            'page_obj': page_obj,
        }
        return render(request, "blog/blog.html", context)

    else:

        # Obtengo todos los posts
        posts = Articulo.objects.all()
        # Obtengo todas las categorías
        categorias = Categoria.objects.all()
        # Obtengo los últimos 6 artículos ordenados por fecha de creación
        ultimos_post = Articulo.objects.filter(publicado=True).order_by('-creacion')[:6]
        # Obtengo todas las etiquetas
        etiquetas = Etiqueta.objects.all()
        # renderizo 4 post por página
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'posts': posts,
            'categorias': categorias,
            'ultimos_post': ultimos_post,
            'etiquetas': etiquetas,
            'page_obj': page_obj,
        }
        return render(request, "blog/blog.html", context)


def post(request, post_id):
    post = get_object_or_404(Articulo, pk=post_id)

    # Obtengo todas las categorías
    categorias = Categoria.objects.all()

    # Obtengo los últimos 6 artículos ordenados por fecha de creación
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
    etiquetas = Etiqueta.objects.filter(articulo__id=post_id)
    print(f"{etiquetas}")

    context = {
        'post': post,
        'categorias': categorias,
        'ultimos_post': ultimos_post,
        'comentarios': comentarios,
        'etiquetas': etiquetas,
    }
    
    return render(request, 'post.html', context )


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
        if comentario.id_usuario == request.user or request.user.is_staff:
            comentario.delete()
    return redirect('blog:post', post_id=comentario.id_articulo.id)


# ----------------------------------- Edición de Permisos -----------------------

def is_admin(user):
    return user.is_staff


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

    if request.method == 'POST':
    # if confirmacion:
        post.delete()
        return redirect('blog:blog')

    return render(request, 'eliminar_post.html', {'post': post})


def modify_user(request):
    if request.user.is_anonymous:
        return redirect('blog:index')
    if request.method == 'POST':
        form = ModificarUsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = ModificarUsuarioForm(instance=request.user)

    return render(request, 'modify_user.html', {'form': form})


#################################### Bloque creación edición de categorías ##########



def crear_editar_categorias(request):
    categorias = Categoria.objects.all()
    categoria_seleccionada = None

    if request.method == 'POST':
        if 'categoria_seleccionada' in request.POST and request.POST['categoria_seleccionada'] != '':
            # If a category is selected, edit it
            categoria_seleccionada = get_object_or_404(Categoria, pk=request.POST['categoria_seleccionada'])
            form = CategoriaCrearEditarForm(request.POST, instance=categoria_seleccionada)
            if 'eliminar_categoria' in request.POST:
                categoria_seleccionada.delete()
                return redirect('blog:crear_editar_categorias')
        else:
            # If no category is selected, create a new one
            form = CategoriaCrearEditarForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('blog:crear_editar_categorias')

    else:
        id_categoria = request.GET.get('categoria_seleccionada')
        if id_categoria:
            categoria_seleccionada = get_object_or_404(Categoria, pk=id_categoria)
            form = CategoriaCrearEditarForm(instance=categoria_seleccionada)
        else:
            form = CategoriaCrearEditarForm()

    return render(request, 'crear_editar_categorias.html', {'form': form, 'categorias': categorias, 'categoria_seleccionada': categoria_seleccionada})




from django.http import JsonResponse
def categoria_json(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    data = {
        'nombre': categoria.nombre,
        'activo': categoria.activo,
        'descripcion': categoria.descripcion,
    }
    return JsonResponse(data)


#################### Bloque edición etiqueta ###################

# def crear_editar_etiqueta(request, id_etiqueta=None):
#     etiqueta = get_object_or_404(Etiqueta, pk=id_etiqueta) if id_etiqueta else None

#     if request.method == 'POST':
#         if 'eliminar' in request.POST and etiqueta:
#             etiqueta.delete()
#             return redirect('blog:crear_editar_etiqueta')  # Reemplaza esto con la URL de la lista de etiquetas

#         form = EtiquetaForm(request.POST, instance=etiqueta)
#         if form.is_valid():
#             form.save()
#             return redirect('blog:crear_editar_etiqueta')  # Reemplaza esto con la URL de la lista de etiquetas

#     else:
#         form = EtiquetaForm(instance=etiqueta)

#     return render(request, 'manage_tags.html', {'form': form, 'etiqueta': etiqueta})
from django.contrib import messages

def crear_editar_etiqueta(request):
    etiqueta_id = request.GET.get('id_etiqueta', None)
    etiqueta = get_object_or_404(Etiqueta, pk=etiqueta_id) if etiqueta_id else None
    etiquetas_existentes = Etiqueta.objects.all()

    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)

        if form.is_valid():
            form.save()
            if etiqueta:
                messages.success(request, 'Etiqueta actualizada exitosamente.')
            else:
                messages.success(request, 'Etiqueta creada exitosamente.')
            return redirect('blog:crear_editar_etiqueta')

        # Obtener el formulario de eliminación de etiquetas seleccionadas
        if 'eliminar_seleccionadas' in request.POST:
            etiquetas_seleccionadas = request.POST.getlist('eliminar_etiqueta')
            if etiquetas_seleccionadas:
                etiquetas_eliminar = Etiqueta.objects.filter(pk__in=etiquetas_seleccionadas)
                etiquetas_eliminar.delete()
                messages.success(request, 'Etiquetas eliminadas exitosamente.')
                return redirect('blog:crear_editar_etiqueta')

    else:
        form = EtiquetaForm(instance=etiqueta)

    return render(request, 'manage_tags.html', {'form': form, 'etiquetas_existentes': etiquetas_existentes, 'etiqueta': etiqueta})


def buscar_articulo(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        palabras = query.split()
        print(f"palabras: {palabras}")
        consulta = Q()

        for palabra in palabras:
            consulta |= Q(contenido__icontains=palabra) | Q(etiqueta__nombre__icontains=palabra)
        print(consulta)    

        posts = Articulo.objects.filter(consulta).distinct()

        for articulo in posts:
            print(articulo.titulo)

        categorias = Categoria.objects.all()
        # Obtengo los últimos 6 artículos ordenados por fecha de creación
        ultimos_post = Articulo.objects.filter(publicado=True).order_by('-creacion')[:6]

        # Obtengo todas las etiquetas
        etiquetas = Etiqueta.objects.all()

        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        print(page_number)
        context = {
                # 'posts': posts,
                'categorias': categorias,
                'ultimos_post': ultimos_post,
                'etiquetas': etiquetas,
                'page_obj': page_obj,
            }

        return render(request, 'blog/blog.html', context)
    else:

        return redirect("blog:blog") 
