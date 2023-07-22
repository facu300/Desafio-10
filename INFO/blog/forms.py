from django import forms
from .models import Articulo, Categoria, Etiqueta, Usuarios, Comentario, Categoria_Articulo
from django.contrib.auth.forms import UserCreationForm

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'bajada', 'contenido', 'imagen', 'publicado', 'categoria', 'autor', 'etiqueta']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'activo', 'descripcion']

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre', 'activo']

class UsuariosForm(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuarios
        fields = ['username','email']


class PermisosUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['es_publico', 'es_colaborador', 'is_staff']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['id_articulo', 'id_usuario', 'contenido', 'fecha_hora', 'estado']

class CategoriaArticuloForm(forms.ModelForm):
    class Meta:
        model = Categoria_Articulo
        fields = ['id_articulo', 'id_categoria']
