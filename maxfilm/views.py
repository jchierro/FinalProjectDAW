from django.shortcuts import render, render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from tmdb3 import set_key
from tmdb3 import Movie
from tmdb3 import set_locale

set_key('c1b10ae4b99ead975d0cbaf0d1045bf0')
set_locale("es")


def index(request):
    """View index"""
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    x = Movie.mostpopular()[:500]
    y = Movie.upcoming()[:5]
    y.sort(key=lambda Movie: Movie.releasedate)

    p = Paginator(x, 12)
    result = p.page(page)
    return render_to_response('maxfilm/index.html', {"result": result,
                                                     "slider": y})


def viewItem(request, id):
    """View any item"""
    return render(request, 'maxfilm/viewItem.html', {"x": Movie(id)})
