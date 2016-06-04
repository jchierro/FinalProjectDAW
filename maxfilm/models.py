# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class AccionPelicula(models.Model):
    """Class AccionPelicula"""
    id_MovieAPI = models.CharField(max_length=20)
    titulo = models.CharField(max_length=60)
    img_portada = models.CharField(max_length=300, null=True)
    pendiente = models.BooleanField()
    vista = models.BooleanField()
    favorita = models.BooleanField()
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Acciones Películas"

    def __str__(self):
        return "ID API: " + self.id_MovieAPI

    def __unicode__(self):
        return "ID API: " + self.id_MovieAPI


class AccionSerie(models.Model):
    """Class AccionSerie"""
    id_SerieAPI = models.CharField(max_length=20)
    titulo = models.CharField(max_length=60)
    img_portada = models.CharField(max_length=300, null=True)
    pendiente = models.BooleanField()
    vista = models.BooleanField()
    favorita = models.BooleanField()
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Acciones Series"

    def __str__(self):
        return "ID API: " + self.id_SerieAPI

    def __unicode__(self):
        return "ID API: " + self.id_SerieAPI


class AccionPersona(models.Model):
    """Class AccionPersona"""
    id_PersonAPI = models.CharField(max_length=20)
    nombre = models.CharField(max_length=60)
    img_perfil = models.CharField(max_length=300, null=True)
    favorita = models.BooleanField()
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Acciones Personas"

    def __str__(self):
        return "ID API: " + self.id_PersonAPI

    def __unicode__(self):
        return "ID API: " + self.id_PersonAPI


class Coleccion(models.Model):
    """Class Colecciones"""
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=150)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    coleccion_media = (
        ('Películas', 'Películas'),
        ('Series', 'Series')
    )
    media = models.CharField(max_length=10, choices=coleccion_media, default=0)
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Colecciones"

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre


class ContenidoMultimedia(models.Model):
    "Class ContenidoMultimedia"
    id_contentAPI = models.CharField(max_length=20)
    titulo = models.CharField(max_length=60)
    img_portada = models.CharField(max_length=300, null=True)
    id_coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Contenidos Multimedia"

    def __str__(self):
        return self.titulo

    def __unicode__(self):
        return self.titulo
