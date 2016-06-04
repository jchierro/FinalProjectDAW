# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccionPelicula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_MovieAPI', models.CharField(max_length=20)),
                ('titulo', models.CharField(max_length=60)),
                ('img_portada', models.CharField(max_length=300, null=True)),
                ('pendiente', models.BooleanField()),
                ('vista', models.BooleanField()),
                ('favorita', models.BooleanField()),
                ('id_usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Acciones Pel\xedculas',
            },
        ),
        migrations.CreateModel(
            name='AccionPersona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_PersonAPI', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=60)),
                ('img_perfil', models.CharField(max_length=300, null=True)),
                ('favorita', models.BooleanField()),
                ('id_usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Acciones Personas',
            },
        ),
        migrations.CreateModel(
            name='AccionSerie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_SerieAPI', models.CharField(max_length=20)),
                ('titulo', models.CharField(max_length=60)),
                ('img_portada', models.CharField(max_length=300, null=True)),
                ('pendiente', models.BooleanField()),
                ('vista', models.BooleanField()),
                ('favorita', models.BooleanField()),
                ('id_usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Acciones Series',
            },
        ),
        migrations.CreateModel(
            name='Coleccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=150)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('media', models.CharField(default=0, max_length=10, choices=[('Pel\xedculas', 'Pel\xedculas'), ('Series', 'Series')])),
                ('id_usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Colecciones',
            },
        ),
        migrations.CreateModel(
            name='ContenidoMultimedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_contentAPI', models.CharField(max_length=20)),
                ('titulo', models.CharField(max_length=60)),
                ('img_portada', models.CharField(max_length=300, null=True)),
                ('id_coleccion', models.ForeignKey(to='maxfilm.Coleccion')),
            ],
            options={
                'verbose_name_plural': 'Contenidos Multimedia',
            },
        ),
    ]
