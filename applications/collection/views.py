

from applications.auth.decorators import checks_permissions, require_permissions
from applications.collection import models
from applications.shortcuts import render_to_response


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

