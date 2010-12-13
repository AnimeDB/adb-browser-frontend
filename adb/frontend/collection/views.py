from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse

from adb.frontend.auth.decorators import (checks_permissions,
                                          require_permissions,
                                          permission_required)
from adb.frontend.collection import models
from adb.frontend.collection import forms
from adb.frontend.shortcuts import render_to_response


@checks_permissions
def browse(request, model=None, letter=None):
    require_permissions(request.user, 'collection.browse_%s' % model)
    
    types = {
        'movies': (models.Movie, 'title'),
        'genres': (models.Genre, 'name'),
        'actors': (models.Actor, 'name'),
    }
    
    items = ()
    
    if model:
        model_class, key = types[model]
        
        if letter:
            letter = letter.upper()
            
            if letter == models.letters[-2]:
                items = model_class.objects.filter(**{
                    '%s__regex' % key: r'^\d.*',
                })
            elif letter == models.letters[-1]:
                items = model_class.objects.filter(**{
                    '%s__regex' % key: r'^\W.*',
                })
            else:
                items = model_class.objects.filter(**{
                    '%s__istartswith' % key: letter,
                })
    else:
        model = 'all'
    
    return render_to_response('collection/browse/%s.html' % model, {
        'letter': letter,
        'items': items,
        'model': model,
    }, request)


@permission_required('collection.display_movie')
def movie(request, movieid):
    movie = get_object_or_404(models.Movie, pk=int(movieid))
    
    if request.user.is_authenticated:
        queryset = request.user.list_set
        initial = {'lists': movie.list_set.all()}
        
        if request.method == 'POST':
            listform = forms.MovieListsForm(queryset, request.POST, initial=initial)
            
            if listform.is_valid():
                movie.list_set.clear()
                movie.list_set.add(*listform.cleaned_data['lists'])
                movie.save()
                
                if request.is_ajax():
                    # Avoid to render full template for an ajax request
                    print "Not rendering tpl"
                    return HttpResponse()
                
        listform = forms.MovieListsForm(queryset, initial=initial)
    else:
        listform = None
    
    return render_to_response('collection/details/movie.html', {
        'movie': movie,
        'listform': listform,
    }, request)


@permission_required('collection.display_genre')
def genre(request, genreid):
    genre = get_object_or_404(models.Genre, pk=int(genreid))
    
    return render_to_response('collection/browse/genre.html', {
        'genre': genre,
        'items': genre.movie_set.all(),
    }, request)


@permission_required('collection.display_actor')
def actor(request, actorid):
    actor = get_object_or_404(models.Actor, pk=int(actorid))
    
    return render_to_response('collection/browse/actor.html', {
        'actor': actor,
        'items': actor.movie_set.all(),
    }, request)
    