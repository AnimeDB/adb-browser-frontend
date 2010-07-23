from django.db import models
from django.contrib.auth.models import User

letters = map(chr, range(ord('A'), ord('Z') + 1)) + ['09', '@!']
letters_set = set(letters)

class Timedelta(object):
    """
    Provides a simpler timedelta object, which holds minutes of duration and
    can return either the whole duration in minutes or splitted up in hours
    and remaining minutes.
    """
    
    def __init__(self, minutes):
        self._minutes = int(minutes or 0)
    
    @property
    def duration(self):
        """
        The total duration of this timedelta, in minutes.
        """
        return self._minutes
    
    @property
    def hours(self):
        """
        The hours of duration of the timedelta, truncated to the integer part.
        """
        return self._minutes // 60
        
    @property
    def minutes(self):
        """
        The minutes of duration of the timedelta, minus whole hours.
        
        For a timedelta with a total duration of 95 minutes, this property
        will be set to a value of 35.
        """
        return self._minutes % 60
    
    def __eq__(self, other):
        return self.duration == other.duration
    
    def __str__(self):
        return str(self.duration)

class DurationField(models.IntegerField):
    """
    A custom field for the django ORM which adds support for a Timedelta data
    type, backed by an integer field.
    """
    
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        if isinstance(value, Timedelta):
            return value
        
        return Timedelta(value)
        
    def get_prep_value(self, value):
        return value.duration

class List(models.Model):
    """
    A custom list tied to a given user.
    """
    
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    movies = models.ManyToManyField('Movie')
    
    class Meta:
        unique_together = (
            ('name', 'user'),
        )
        
        permissions = (
            ("can_use_lists", "Can use lists"),
        )
    
    def __str__(self):
        return self.name.encode('utf-8')
    
    def __unicode__(self):
        return self.name
    
class Genre(models.Model):
    """
    A film genre identified in the system with a unique name.
    """
    name = models.CharField(unique=True, max_length=100)
    
    def __unicode__(self):
        return self.name

class Actor(models.Model):
    """
    An actor identified in the system with a unique name.
    """
    name = models.CharField(unique=True, max_length=100)
    
    def __unicode__(self):
        return self.name

class Movie(models.Model):
    """
    A movie along with its metadata.
    """
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100, null=True, blank=True)
    
    genres = models.ManyToManyField(Genre)
    cast = models.ManyToManyField(Actor)
    year = models.PositiveSmallIntegerField()
    duration = DurationField()
    plot = models.TextField(blank=True, null=True)
    
    meta_origin = models.URLField(verify_exists=False)
    poster_origin = models.URLField(verify_exists=False, blank=True, null=True)
    
    class Meta:
        permissions = (
            ('can_browse', 'Can browse movies'),
        )
        
        ordering = (
            'title',
            'original_title',
            'year',
            'duration'
        )
    
    def __unicode__(self):
        return u'%s (%d)' % (self.title, self.year)

#class MoreLink(models.Model):
#    """
#    A link to an external resource describing the movie
#    """
#    title = models.CharField(max_length=100)
#    url = models.URLField(verify_exists=False)
#    visits = models.PositiveIntegerField(default=0)
#    movie = models.ForeignKey(Movie, related_name='links')

class Service(models.Model):
    """
    The service used to publish a release.
    """
    name = models.CharField(unique=True, max_length=100)
    domain = models.CharField(unique=True, max_length=100)

class Release(models.Model):
    """
    A release bound to a movie which groups one or more links to the actual
    content.
    """
    movie = models.ForeignKey(Movie)
    service = models.ForeignKey(Service)
    user = models.ForeignKey(User)
    rating = models.FloatField(default=0)
    votes = models.PositiveIntegerField(default=0)

class Link(models.Model):
    """
    A link to the whole or partial content of a release.
    """
    title = models.CharField(max_length=100)
    url = models.URLField(verify_exists=False)
    visits = models.PositiveIntegerField(default=0)
    release = models.ForeignKey(Release, related_name='links')
