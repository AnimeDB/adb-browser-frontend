from django.db import models
from django.contrib.auth.models import User

class List(models.Model):
    """
    A custom list tied to a given user.
    """
    
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    movies = models.ManyToManyField('collection.Movie')
    
    class Meta:
        unique_together = (
            ('name', 'user'),
        )
        
        ordering = ('name', 'user')
        
        permissions = (
            ("view_list", "Can view list"),
            ("browse_lists", "Can browse lists"),
        )
    
    @models.permalink
    def get_absolute_url(self):
        return ('lists:view', (), {'id': str(self.id)})
        
    
    def __str__(self):
        return self.name.encode('utf-8')
    
    def __unicode__(self):
        return self.name