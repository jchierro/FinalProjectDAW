from django.shortcuts import render, render_to_response
from forms import SignUpForm
from django.http import HttpResponse, HttpResponseNotFound, Http404
import json
from urllib2 import Request, urlopen, HTTPError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib.auth.hashers import make_password

headers = {
    'Accept': 'application/json',
    }


def login(request):
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
    del request.session['login']
    auth.logout(request)

    return HttpResponseRedirect('/')


def signup(request):
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

    if request.method == 'POST':
        aux = User.objects.get(username=request.user.username)
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

    return render(request, 'maxfilm/dashboard.html', {'default': True})


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

    return render(request, 'maxfilm/viewMovie.html', {'movie': movie,
                                                      'credits': credits,
                                                      'videos': videos,
                                                      'similar': similar})


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

    return render(request, 'maxfilm/viewTv.html', {'tv': tv,
                                                   'credits': credits,
                                                   'similar': similar,
                                                   'videos': videos,
                                                   'seasons': seasons})


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

    return render(request, 'maxfilm/viewPerson.html', {'person': person,
                                                       'images': images,
                                                       'credits': credits})


def Search(request):
    """Search"""
    if request.method == "GET":
        text = str(request.GET["text"]).replace(" ", ",")
    else:
        text = ","

    con = Request('http://api.themoviedb.org/3/search/movie/' +
                  '?query=' + text +
                  '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    resultMovie = json.loads(urlopen(con).read())

    con = Request('http://api.themoviedb.org/3/search/tv/' +
                  '?query=' + text +
                  '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    resultTv = json.loads(urlopen(con).read())

    con = Request('http://api.themoviedb.org/3/search/person/' +
                  '?query=' + text +
                  '&api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
                  headers=headers)
    resultPeople = json.loads(urlopen(con).read())

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
