from haystack import site
from haystack.indexes import *

from adb.frontend.collection.models import Movie

class MovieIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    #cast = CharField(model_attr='cast')
    #genres = DateTimeField(model_attr='genres')
    #duration = 

site.register(Movie, MovieIndex)