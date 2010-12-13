from django.db import models
from django.db.models.signals import post_save
#from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    animedb_userid = models.PositiveIntegerField(blank=True, null=True, unique=True)
    
    @classmethod
    def create_profile(cls, sender, **kwargs):
        if kwargs['created']:
            cls(user=kwargs['instance']).save()

post_save.connect(UserProfile.create_profile, sender=User)
