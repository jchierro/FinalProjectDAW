"""."""
from django.shortcuts import render
from tmdb3 import set_key
from tmdb3 import Series


def index(request):
    """."""
    set_key('c1b10ae4b99ead975d0cbaf0d1045bf0')
    result = Series(1412)
    return render(request, 'maxfilm/index.html', {"result": result})
