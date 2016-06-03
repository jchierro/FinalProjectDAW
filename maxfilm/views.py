# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, redirect
from forms import SignUpForm, CollectionForm
from django.http import HttpResponse, HttpResponseNotFound, Http404
import json
import urllib
from urllib2 import Request, urlopen, HTTPError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from models import AccionPelicula, AccionSerie, AccionPersona, Coleccion, ContenidoMultimedia

headers = {
    'Accept': 'application/json',
    }


def login(request):
    """Login"""

    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        request.session['login'] = user.first_name
        return HttpResponseRedirect("/dashboard/")
    else:
        request.session['login'] = 'error'
        return HttpResponseRedirect('/')


def logout(request):
    """Logout"""

    del request.session['login']
    auth.logout(request)

    return HttpResponseRedirect('/')


def signup(request):
    """Signup"""

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            user.save()

            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()

    data = {
        'form': form,
    }

    return render_to_response('maxfilm/signup.html', data,
                              context_instance=RequestContext(request))


@login_required
def dashboard(request):
    """Dashboard of the user"""

    if request.method == 'POST' and 'collections' not in request.GET and 'updateCollection' not in request.GET:
        aux = User.objects.get(username=request.user.username)
        if request.POST['password'] != '':
            aux.password = make_password(request.POST['password'])
        aux.email = request.POST['email']
        aux.first_name = request.POST['first_name']
        aux.last_name = request.POST['last_name']
        aux.save()

        return render(request, 'maxfilm/dashboard.html', {'profile': True,
                                                          'auxUser': aux,
                                                          'alert': True})

    if 'profile' in request.GET:
        aux = User.objects.get(username=request.user.username)

        return render(request, 'maxfilm/dashboard.html', {'profile': True,
                                                          'auxUser': aux})

    if 'movies' in request.GET:
        bookmarks = AccionPelicula.objects.filter(id_usuario=request.user).filter(favorita=True)
        pending = AccionPelicula.objects.filter(id_usuario=request.user).filter(pendiente=True)
        viewed = AccionPelicula.objects.filter(id_usuario=request.user).filter(vista=True)

        return render(request, 'maxfilm/dashboard.html', {'bookmarks': bookmarks,
                                                          'pending': pending,
                                                          'viewed': viewed,
                                                          'movies': True})

    if 'tv' in request.GET:
        bookmarks = AccionSerie.objects.filter(id_usuario=request.user).filter(favorita=True)
        pending = AccionSerie.objects.filter(id_usuario=request.user).filter(pendiente=True)
        viewed = AccionSerie.objects.filter(id_usuario=request.user).filter(vista=True)

        return render(request, 'maxfilm/dashboard.html', {'bookmarks': bookmarks,
                                                          'pending': pending,
                                                          'viewed': viewed,
                                                          'tv': True})

    if 'people' in request.GET:
        bookmarks = AccionPersona.objects.filter(id_usuario=request.user).filter(favorita=True)

        return render(request, 'maxfilm/dashboard.html', {'bookmarks': bookmarks,
                                                          'people': True})

    if 'deleteCollection' in request.GET:
        Coleccion.objects.get(id=request.GET['id']).delete()

        return redirect('/dashboard?collections')

    if 'updateCollection' in request.GET:
        aux = Coleccion.objects.get(id=request.GET['id'])

        if request.method == 'POST':
            aux.nombre = request.POST['nombre']
            aux.descripcion = request.POST['descripcion']
            aux.save()

            return HttpResponseRedirect('/dashboard/?collections')

        return render(request, 'maxfilm/dashboard.html', {'collection': aux,
                                                          'editCollection': True})

    if 'delete' in request.GET:
        ContenidoMultimedia.objects.filter(id=request.GET['id']).delete()

        return redirect('/dashboard?collections')

    if 'viewC' in request.GET:
        aux = Coleccion.objects.get(id=request.GET['id'])
        collection = ContenidoMultimedia.objects.filter(id_coleccion=aux)

        return render(request, 'maxfilm/dashboard.html', {'collection': collection,
                                                          'viewCollection': True,
                                                          'media': aux.media,
                                                          'nombre': aux.nombre})

    if 'collections' in request.GET:
        collectionsMovies = Coleccion.objects.filter(id_usuario=request.user).filter(media='Películas')
        collectionsTv = Coleccion.objects.filter(id_usuario=request.user).filter(media='Series')

        if request.method == 'POST':
            form = CollectionForm(request.POST)
            if form.is_valid():
                aux = Coleccion()
                aux.nombre = form.cleaned_data["nombre"]
                aux.descripcion = form.cleaned_data["descripcion"]
                aux.media = form.cleaned_data["media"]
                aux.id_usuario = request.user
                aux.save()

                return HttpResponseRedirect('/dashboard/?collections')
        else:
            form = CollectionForm()

        return render(request, 'maxfilm/dashboard.html', {'collections': True,
                                                          'form': form,
                                                          'collectionsTv': collectionsTv,
                                                          'collectionsMovies': collectionsMovies})

    total = AccionPelicula.objects.count()
    bookmarkMovie = AccionPelicula.objects.filter(favorita=True).count()
    pendingMovie = AccionPelicula.objects.filter(pendiente=True).count()
    viewedMovie = AccionPelicula.objects.filter(vista=True).count()
    dataMovie = {'bookmarkMovie': bookmarkMovie,
                 'pendingMovie': pendingMovie,
                 'viewedMovie': viewedMovie,
                 'total': total}

    total = AccionSerie.objects.count()
    bookmarkTv = AccionSerie.objects.filter(favorita=True).count()
    pendingTv = AccionSerie.objects.filter(pendiente=True).count()
    viewedTv = AccionSerie.objects.filter(vista=True).count()
    dataTv = {'bookmarkTv': bookmarkTv,
              'pendingTv': pendingTv,
              'viewedTv': viewedTv,
              'total': total}

    return render(request, 'maxfilm/dashboard.html', {'default': True,
                                                      'dataMovie': dataMovie,
                                                      'dataTv': dataTv})


def viewed(request):
    """Viewed"""

    if 'movie' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/movie/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        movie = json.loads(urlopen(con).read())

        try:
            aux = AccionPelicula.objects.filter(id_usuario=request.user.id).get(id_MovieAPI=request.GET['id'])
            aux.pendiente = False
            aux.vista = True
            aux.save()
        except AccionPelicula.DoesNotExist:
            aux = AccionPelicula()
            aux.id_MovieAPI = movie['id']
            aux.titulo = movie['title']
            aux.img_portada = movie['poster_path']
            aux.pendiente = False
            aux.vista = True
            aux.favorita = False
            aux.id_usuario = request.user
            aux.save()

        return redirect('/movie/' + request.GET['id'])

    if 'movie' in request.GET and 'delete' in request.GET:
        aux = AccionPelicula.objects.get(id=request.GET['id'])

        if aux.pendiente is False and aux.favorita is False:
            aux.delete()
        else:
            aux.vista = False
            aux.save()

        return redirect('/dashboard?movies')

    if 'tv' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/tv/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        tv = json.loads(urlopen(con).read())

        try:
            aux = AccionSerie.objects.filter(id_usuario=request.user.id).get(id_SerieAPI=request.GET['id'])
            aux.pendiente = False
            aux.vista = True
            aux.save()
        except AccionSerie.DoesNotExist:
            aux = AccionSerie()
            aux.id_SerieAPI = tv['id']
            aux.titulo = tv['name']
            aux.img_portada = tv['poster_path']
            aux.pendiente = False
            aux.vista = True
            aux.favorita = False
            aux.id_usuario = request.user
            aux.save()

        return redirect('/tv/' + request.GET['id'])

    if 'tv' in request.GET and 'delete' in request.GET:
        aux = AccionSerie.objects.get(id=request.GET['id'])

        if aux.pendiente is False and aux.favorita is False:
            aux.delete()
        else:
            aux.vista = False
            aux.save()

        return redirect('/dashboard?tv')


def pending(request):
    """Pending"""

    if 'movie' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/movie/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        movie = json.loads(urlopen(con).read())

        try:
            aux = AccionPelicula.objects.filter(id_usuario=request.user.id).get(id_MovieAPI=request.GET['id'])
            aux.pendiente = True
            aux.vista = False
            aux.save()
        except AccionPelicula.DoesNotExist:
            aux = AccionPelicula()
            aux.id_MovieAPI = movie['id']
            aux.titulo = movie['title']
            aux.img_portada = movie['poster_path']
            aux.pendiente = True
            aux.vista = False
            aux.favorita = False
            aux.id_usuario = request.user
            aux.save()

        return redirect('/movie/' + request.GET['id'])

    if 'movie' in request.GET and 'delete' in request.GET:
        aux = AccionPelicula.objects.get(id=request.GET['id'])

        if aux.vista is False and aux.favorita is False:
            aux.delete()
        else:
            aux.pendiente = False
            aux.save()

        return redirect('/dashboard?movies')

    if 'tv' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/tv/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        tv = json.loads(urlopen(con).read())

        try:
            aux = AccionSerie.objects.filter(id_usuario=request.user.id).get(id_SerieAPI=request.GET['id'])
            aux.pendiente = True
            aux.vista = False
            aux.save()
        except AccionSerie.DoesNotExist:
            aux = AccionSerie()
            aux.id_SerieAPI = tv['id']
            aux.titulo = tv['name']
            aux.img_portada = tv['poster_path']
            aux.pendiente = True
            aux.vista = False
            aux.favorita = False
            aux.id_usuario = request.user
            aux.save()

        return redirect('/tv/' + request.GET['id'])

    if 'tv' in request.GET and 'delete' in request.GET:
        aux = AccionSerie.objects.get(id=request.GET['id'])

        if aux.vista is False and aux.favorita is False:
            aux.delete()
        else:
            aux.pendiente = False
            aux.save()

        return redirect('/dashboard?tv')


def bookmark(request):
    """Bookmark"""

    if 'movie' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/movie/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        movie = json.loads(urlopen(con).read())

        try:
            aux = AccionPelicula.objects.filter(id_usuario=request.user.id).get(id_MovieAPI=request.GET['id'])
            aux.favorita = True
            aux.save()
        except AccionPelicula.DoesNotExist:
            aux = AccionPelicula()
            aux.id_MovieAPI = movie['id']
            aux.titulo = movie['title']
            aux.img_portada = movie['poster_path']
            aux.pendiente = False
            aux.vista = False
            aux.favorita = True
            aux.id_usuario = request.user
            aux.save()

        return redirect('/movie/' + request.GET['id'])

    if 'movie' in request.GET and 'delete' in request.GET:
        aux = AccionPelicula.objects.get(id=request.GET['id'])

        if aux.vista is False and aux.pendiente is False:
            aux.delete()
        else:
            aux.favorita = False
            aux.save()

        return redirect('/dashboard?movies')

    if 'tv' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/tv/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        tv = json.loads(urlopen(con).read())

        try:
            aux = AccionSerie.objects.filter(id_usuario=request.user.id).get(id_SerieAPI=request.GET['id'])
            aux.favorita = True
            aux.save()
        except AccionSerie.DoesNotExist:
            aux = AccionSerie()
            aux.id_SerieAPI = tv['id']
            aux.titulo = tv['name']
            aux.img_portada = tv['poster_path']
            aux.pendiente = False
            aux.vista = False
            aux.favorita = True
            aux.id_usuario = request.user
            aux.save()

        return redirect('/tv/' + request.GET['id'])

    if 'tv' in request.GET and 'delete' in request.GET:
        aux = AccionSerie.objects.get(id=request.GET['id'])

        if aux.vista is False and aux.pendiente is False:
            aux.delete()
        else:
            aux.favorita = False
            aux.save()

        return redirect('/dashboard?tv')

    if 'person' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/person/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        person = json.loads(urlopen(con).read())
        aux = AccionPersona()
        aux.id_PersonAPI = person['id']
        aux.nombre = person['name']
        aux.img_perfil = person['profile_path']
        aux.favorita = True
        aux.id_usuario = request.user
        aux.save()

        return redirect('/person/' + request.GET['id'])

    if 'person' in request.GET and 'delete' in request.GET:
        AccionPersona.objects.get(id=request.GET['id']).delete()

        return redirect('/dashboard?people')

    return redirect('/')


def add(request):
    """Add"""

    if 'movie' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/movie/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        movie = json.loads(urlopen(con).read())

        try:
            aux = ContenidoMultimedia.objects.filter(id_coleccion=request.GET['idCollection']).get(id_contentAPI=request.GET['id'])
        except ContenidoMultimedia.DoesNotExist:
            aux = ContenidoMultimedia()
            aux.id_contentAPI = movie['id']
            aux.titulo = movie['title']
            aux.img_portada = movie['poster_path']
            aux.id_coleccion = Coleccion.objects.get(id=request.GET['idCollection'])
            aux.save()

        return redirect('/movie/' + request.GET['id'])

    if 'tv' in request.GET and 'delete' not in request.GET:
        con = Request('http://api.themoviedb.org/3/tv/' + request.GET['id'] +
                      '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        tv = json.loads(urlopen(con).read())

        try:
            aux = ContenidoMultimedia.objects.filter(id_coleccion=request.GET['idCollection']).get(id_contentAPI=request.GET['id'])
        except ContenidoMultimedia.DoesNotExist:
            aux = ContenidoMultimedia()
            aux.id_contentAPI = tv['id']
            aux.titulo = tv['name']
            aux.img_portada = tv['poster_path']
            aux.id_coleccion = Coleccion.objects.get(id=request.GET['idCollection'])
            aux.save()

        return redirect('/tv/' + request.GET['id'])

    return redirect('/')


def index(request):
    """View index"""

    con = Request('http://api.tviso.com/auth_token?id_api=3489&secret=nCHkh3DheNRqNcR497aC',
                  headers=headers)
    apiCode = json.loads(urlopen(con).read())['auth_token']

    con = Request('http://api.themoviedb.org/3/movie/upcoming?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    upComing = json.loads(urlopen(con).read())['results'][:5]

    con = Request('http://api.tviso.com/news/promoted?auth_token=' + apiCode, headers=headers)
    news = json.loads(urlopen(con).read())['results'][:12]

    for new in news:
        new['title'] = new['title'].replace("&#039;", "'")
        new['short_text'] = new['short_text'].replace("&#039;", "'")

    return render_to_response('maxfilm/index.html', {"slider": upComing,
                                                     "news": news},
                              context_instance=RequestContext(request))


def viewMovie(request, id):
    """View any Movie"""
    con = Request('http://api.themoviedb.org/3/movie/' + id +
                  '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    movie = json.loads(urlopen(con).read())

    con = Request('http://api.themoviedb.org/3/movie/' + id +
                  '/credits?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    credits = json.loads(urlopen(con).read())

    con = Request('http://api.themoviedb.org/3/movie/' + id +
                  '/videos?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    videos = json.loads(urlopen(con).read())['results']

    con = Request('http://api.themoviedb.org/3/movie/' + id +
                  '/similar?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    similar = json.loads(urlopen(con).read())['results'][:6]

    try:
        aux = AccionPelicula.objects.filter(id_usuario=request.user.id).get(id_MovieAPI=id)

        if aux.favorita:
            bookmark = True
        else:
            bookmark = False

        if aux.pendiente or aux.vista:
            viewing = True
        else:
            viewing = False
    except AccionPelicula.DoesNotExist:
        bookmark = False
        viewing = False

    collections = Coleccion.objects.filter(id_usuario=request.user.id).filter(media='Películas')

    return render(request, 'maxfilm/viewMovie.html', {'movie': movie,
                                                      'credits': credits,
                                                      'videos': videos,
                                                      'similar': similar,
                                                      'bookmark': bookmark,
                                                      'viewing': viewing,
                                                      'collections': collections})


def viewTv(request, id):
    """View Tv"""
    con = Request('http://api.themoviedb.org/3/tv/' + id +
                  '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    tv = json.loads(urlopen(con).read())

    con = Request('http://api.themoviedb.org/3/tv/' + id +
                  '/credits?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    credits = json.loads(urlopen(con).read())

    con = Request('http://api.themoviedb.org/3/tv/' + id +
                  '/similar?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    similar = json.loads(urlopen(con).read())['results'][:6]

    con = Request('http://api.themoviedb.org/3/tv/' + id +
                  '/videos?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    videos = json.loads(urlopen(con).read())['results']

    seasons = []
    count = 1
    total = int(tv['number_of_seasons'])

    try:
        while(count <= total):
            con = Request('http://api.themoviedb.org/3/tv/' + id +
                          '/season/' + str(count) + '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                          headers=headers)
            seasons.append(json.loads(urlopen(con).read()))
            count = count + 1
    except HTTPError:
        pass

    try:
        aux = AccionSerie.objects.filter(id_usuario=request.user.id).get(id_SerieAPI=id)

        if aux.favorita:
            bookmark = True
        else:
            bookmark = False

        if aux.vista or aux.pendiente:
            viewing = True
        else:
            viewing = False
    except AccionSerie.DoesNotExist:
        bookmark = False
        viewing = False

    collections = Coleccion.objects.filter(id_usuario=request.user.id).filter(media='Series')

    return render(request, 'maxfilm/viewTv.html', {'tv': tv,
                                                   'credits': credits,
                                                   'similar': similar,
                                                   'videos': videos,
                                                   'seasons': seasons,
                                                   'bookmark': bookmark,
                                                   'viewing': viewing,
                                                   'collections': collections})


def viewPerson(request, id):
    """View Person"""
    con = Request('http://api.themoviedb.org/3/person/' + id +
                  '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    person = json.loads(urlopen(con).read())

    images = []
    try:
        con = Request('http://api.themoviedb.org/3/person/' + id +
                      '/tagged_images?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        images = json.loads(urlopen(con).read())['results'][0]
    except HTTPError, e:
        pass

    con = Request('http://api.themoviedb.org/3/person/' + id +
                  '/combined_credits?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    credits = json.loads(urlopen(con).read())

    try:
        aux = AccionPersona.objects.filter(id_usuario=request.user.id).get(id_PersonAPI=id)

        if aux.favorita:
            bookmark = True
    except AccionPersona.DoesNotExist:
        bookmark = False

    return render(request, 'maxfilm/viewPerson.html', {'person': person,
                                                       'images': images,
                                                       'credits': credits,
                                                       'bookmark': bookmark})


def Search(request):
    """Search"""
    if request.method == "GET":
        text = request.GET["text"].replace(" ", ",")
    else:
        text = ","

    con = u'http://api.themoviedb.org/3/search/movie/' + '?query=' + text + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es'
    resultMovie = json.loads(urllib.urlopen(con.encode("utf-8")).read())

    con = u'http://api.themoviedb.org/3/search/tv/' + '?query=' + text + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es'
    resultTv = json.loads(urllib.urlopen(con.encode("utf-8")).read())

    con = u'http://api.themoviedb.org/3/search/person/' + '?query=' + text + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es'
    resultPeople = json.loads(urllib.urlopen(con.encode("utf-8")).read())

    return render(request, 'maxfilm/search.html', {'resultMovie': resultMovie,
                                                   'resultTv': resultTv,
                                                   'resultPeople': resultPeople})


def Movies(request):
    """Movies in general"""
    movies = []
    num = ''
    page = ''
    flag = True
    result = True
    action = ''

    if 'page' in request.GET:
        page = str(request.GET["page"])
    else:
        page = '1'

    if 'genre' in request.GET:
        num = str(request.GET["genre"])
        con = Request('http://api.themoviedb.org/3/genre/' + num +
                      '/movies?page=' + page + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        movies = json.loads(urlopen(con).read())['results']

    if 'query' in request.GET:
        action = str(request.GET["query"])
        con = Request('http://api.themoviedb.org/3/movie/' + action + '?page=' + page + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        movies = json.loads(urlopen(con).read())['results']
        if action == 'upcoming':
            result = False

    if 'genre' not in request.GET and 'query' not in request.GET:
        con = Request('http://api.themoviedb.org/3/movie/popular?page=' + page + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        movies = json.loads(urlopen(con).read())['results']
        flag = False

    con = Request('http://api.themoviedb.org/3/genre/movie/list?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    genres = json.loads(urlopen(con).read())['genres']

    return render(request, 'maxfilm/movies.html', {'genres': genres,
                                                   'movies': movies,
                                                   'genre': num,
                                                   'page': page,
                                                   'flag': flag,
                                                   'result': result,
                                                   'action': action})


def Tv(request):
    """Content of TV in general"""
    tv = []
    flag = True
    page = ''
    action = ''
    num = ''

    if 'page' in request.GET:
        page = str(request.GET["page"])
    else:
        page = '1'

    if 'genre' in request.GET:
        num = str(request.GET["genre"])
        con = Request('http://api.themoviedb.org/3/discover/tv?with_genres=' + num +
                      '&page=' + page + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        tv = json.loads(urlopen(con).read())['results']

    if 'query' in request.GET:
        action = str(request.GET["query"])
        con = Request('http://api.themoviedb.org/3/tv/' + action + '?page=' + page + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        tv = json.loads(urlopen(con).read())['results']

    if 'genre' not in request.GET and 'query' not in request.GET:
        con = Request('http://api.themoviedb.org/3/tv/popular?page=' + page + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                      headers=headers)
        tv = json.loads(urlopen(con).read())['results']
        flag = False

    con = Request('http://api.themoviedb.org/3/genre/tv/list?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    genres = json.loads(urlopen(con).read())['genres']

    return render(request, 'maxfilm/tv.html', {'genres': genres,
                                               'tv': tv,
                                               'flag': flag,
                                               'page': page,
                                               'action': action,
                                               'genre': num})


def People(request):
    """People who are actors or workers"""
    people = []
    page = ''

    if 'page' in request.GET:
        page = str(request.GET["page"])
    else:
        page = '1'

    con = Request('http://api.themoviedb.org/3/person/popular?page=' + page + '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    people = json.loads(urlopen(con).read())['results']

    return render(request, 'maxfilm/people.html', {'people': people,
                                                   'page': page})
