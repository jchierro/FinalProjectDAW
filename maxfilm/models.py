# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
# from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser


class Usuarios(AbstractBaseUser):
    """Class Usuarios. Bajo pruebas!!"""
    # usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    nombre_usuario = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=60)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='imgPerfil', blank=False, null=False)

    USERNAME_FIELD = 'nombre_usuario'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nombre_usuario

    def __unicode__(self):
        return self.nombre_usuario


class Comentarios(models.Model):
    """Class Comentarios"""
    titulo = models.TextField(max_length=100)
    mensaje = models.TextField(max_length=300)
    fecha = models.DateTimeField(default=timezone.now)
    id_contenidoAPI = models.IntegerField()
    puntuacion = models.IntegerField()
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def __unicode__(self):
        return self.titulo


class Acciones(models.Model):
    """Class Acciones"""
    id_contenidoAPI = models.IntegerField()
    titulo = models.TextField(max_length=100)
    img_contenido = models.CharField(max_length=400)
    pendiente = models.BooleanField()
    vista = models.BooleanField()
    recomendar = models.BooleanField()
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_contenidoAPI

    def __unicode__(self):
        return self.id_contenidoAPI


class MensajesTablon(models.Model):
    """Class MensajesTablon"""
    mensaje = models.TextField(max_length=250)
    fecha = models.DateTimeField(default=timezone.now)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha

    def __unicode__(self):
        return self.fecha


class Colecciones(models.Model):
    """Class Colecciones"""
    nombre = models.CharField(max_length=35)
    descripcion = models.TextField(max_length=100)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre


class ContenidoMultimedia(models.Model):
    "Class ContenidoMultimedia"
    id_contenidoAPI = models.IntegerField()
    titulo = models.CharField(max_length=40)
    img_contenido = models.CharField(max_length=400)
    id_coleccion = models.ForeignKey(Colecciones, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def __unicode__(self):
        return self.titulo
