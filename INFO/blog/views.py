from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.urls import reverse
from django.views import generic
from .forms import UsuariosForm
# from django.contrib.auth.forms import UserCreationForm

def index_view(request):
    context = {
        'is_index': True
    }
    return render(request, 'index.html', context)

def blog(request):
    return render(request, "blog/blog.html")

class BlogView(generic.TemplateView):
    template_name = "blog/base.html"


def post(request):
    return render(request, 'post.html')

# def register_view(request):
#     if request.method == 'POST':
#         # Procesar el formulario si se envió una solicitud POST
#         form = UsuariosForm(request.POST)
#         print('la papa')
#         if form.is_valid():
#             # Aquí puedes guardar los datos del formulario si es válido
#             form.save()
#             # Redireccionar a una página de éxito o hacer algo más
#     else:
#         # Si la solicitud no es POST, mostrar el formulario vacío
#         print('entro acá')
#         form = UsuariosForm()

#     return render(request, 'register.html', {'form': form})

def register_view(request):
    
    if request.method == 'POST':
        form = UsuariosForm(request.POST)
        # Procesar el formulario si se envió una solicitud POST
        if form.is_valid():
            form.save()
            # Redireccionar a una página de éxito o hacer algo más
            return redirect('nombre_de_la_url_de_exito')
        # Si el formulario no es válido, se mostrará con los mensajes de error
    else:
        form = UsuariosForm()
        print(form.errors)
    return render(request, 'register.html', {'form': form})