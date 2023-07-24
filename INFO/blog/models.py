from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.conf import settings # para que funcione el modelo de autenticación modificado

# Create your models here.

class Usuarios(AbstractUser, PermissionsMixin):
    
    
    avatar = models.CharField(max_length=250)
    es_publico = models.BooleanField(default=True)
    es_colaborador = models.BooleanField(default=False)
    

    groups = models.ManyToManyField(
        'auth.Group',  # Modelo relacionado: auth.Group
        blank=True,
        related_name='usuarios_group_set'  # Puedes cambiar 'usuarios_group_set' por el nombre que prefieras
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',  # Modelo relacionado: auth.Permission
        blank=True,
        related_name='usuarios_permission_set'  # Puedes cambiar 'usuarios_permission_set' por el nombre que prefieras
    )

    def __str__(self):
        return self.username


class Categoria(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Etiqueta(models.Model):
        nombre = models.CharField(max_length=200, unique=True)
        activo = models.BooleanField(default=True)
        creacion = models.DateTimeField(auto_now_add=True)
        actualizacion = models.DateTimeField(auto_now=True)
    
        def __str__(self):
            return self.nombre
    
        class Meta:
            ordering = ['nombre']

class Articulo(models.Model):
    titulo = models.CharField(max_length=250)
    bajada = models.CharField(max_length=600)         # este lo llamé así por el desafio 12 que bajaron
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='media', null=True)
    publicado = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=False
    )
    # autor = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    # etiqueta = models.ManyToManyField(Etiqueta, null=True)
    creacion = models.DateTimeField(auto_now_add=True)
    actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-creacion']

class Comentario(models.Model):
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_hora = models.DateTimeField()
    estado = models.BooleanField()


class Categoria_Articulo(models.Model):
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

