from django.contrib.auth.decorators import permission_required
from shortcuts import render_to_response
from django.shortcuts import redirect

from models import letters, letters_set, Movie

@permission_required('collection.can_browse')
def browse(request, letter=None):
    movies = ()
    
    if letter:
        letter = letter.upper()
        
        if letter == letters[-2]:
            movies = Movie.objects.filter(title__regex=r'^\d.*')
        elif letter == letters[-1]:
            movies = Movie.objects.filter(title__regex=r'^\W.*')
        else:
            movies = Movie.objects.filter(title__istartswith=letter)
    
    return render_to_response('collection/browse.html', {
        'letter': letter,
        'letters': letters,
        'movies': movies
    }, request)