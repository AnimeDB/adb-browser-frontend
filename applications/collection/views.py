from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from shortcuts import render_to_response

from applications.collection.models import letters, Movie, Genre, Actor

@permission_required('collection.can_browse')
def browse(request, model=None, letter=None):
    models = {
        'movies': (Movie, 'title'),
        'genres': (Genre, 'name'),
        'actors': (Actor, 'name'),
    }
    
    items = ()
    
    if model:
        model_class, key = models[model]
        
        if letter:
            letter = letter.upper()
            
            if letter == letters[-2]:
                items = model_class.objects.filter(**{
                    '%s__regex' % key: r'^\d.*',
                })
            elif letter == letters[-1]:
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

