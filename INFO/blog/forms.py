from django import forms
from .models import Articulo, Categoria, Etiqueta, Usuarios, Comentario, Categoria_Articulo
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError 
from PIL import Image

class ArticuloForm(forms.ModelForm):
    
    def clean_imagen(self):
        imagen = self.cleaned_data['imagen']

        if imagen:
            img = Image.open(imagen)
            if img.width > 1020 or img.height > 768:
                raise ValidationError("La imagen no puede ser mayor de 1020x768 píxeles.")

        return imagen

    class Meta:
        model = Articulo
        fields = ['titulo', 'bajada', 'contenido', 'imagen']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'activo', 'descripcion']

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre', 'activo']

class UsuariosForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):            # Estas lineas de código borran las helps que
        super().__init__(*args, **kwargs)           # dejan feo el formulario
        self.fields['username'].help_text = None 
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    class Meta:
        model = Usuarios
        fields = ['username','email','first_name', 'last_name']

class LoginForm(AuthenticationForm):
    # Este formulario hereda de AuthenticationForm, por lo que no es necesario agregar campos adicionales.
    # Es solo para importar el formulario y usarlo en las views
    pass


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
