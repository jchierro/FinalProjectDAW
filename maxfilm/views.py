from django.shortcuts import render, render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from tmdb3 import set_locale, set_cache, Movie, set_key
"""import json
from urllib2 import Request, urlopen
headers = {
    'Accept': 'application/json',
    }
con = Request('http://api.themoviedb.org/3/movie/' + id +
              '?api_key=c1b10ae4b99ead975d0cbaf0d1045bf0&language=es',
              headers=headers)
x = json.loads(urlopen(con).read())"""

set_key('c1b10ae4b99ead975d0cbaf0d1045bf0')
set_cache('null')
set_locale("es")


def index(request):
    """View index"""

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    x = Movie.mostpopular()[:50]
    y = Movie.upcoming()[:5]
    y.sort(key=lambda Movie: Movie.releasedate)

    p = Paginator(x, 12)
    result = p.page(page)
    return render_to_response('maxfilm/index.html', {"result": result,
                                                     "slider": y})


def viewItem(request, id):
    """View any item"""

    x = Movie(id)
    y = x.similar[:6]
    z = x.youtube_trailers[0].geturl().split("=")[1]

    return render(request, 'maxfilm/viewItem.html', {"x": x, "y": y, "z": z})
