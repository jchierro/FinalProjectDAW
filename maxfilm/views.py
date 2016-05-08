from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseNotFound, Http404
import json
from urllib2 import Request, urlopen, HTTPError

headers = {
    'Accept': 'application/json',
    }


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
                                                     "news": news})


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
