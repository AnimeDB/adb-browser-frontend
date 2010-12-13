import hashlib

from django.db import connections
from django.contrib.auth.models import User, Group
from django.contrib.auth.backends import ModelBackend

class VBulletinBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        """
        Authenticates against the vBulletin backend and returns the local user.
        If the local user does not exist, then create it with the correct
        username and email.
        The created user will not be able to login against the default database.
        
        @todo: Check that the given username does not exist with a useable
               password.
        """
        
        # @todo: Move the following properties to the settings:
        DATABASE = 'forum_adb2'
        TABLE_NAME = 'users'
        GROUPS = ('Beta testers',)
        
        # Hash the password locally to avoid to transfer it in cleartext on
        # the network
        password = hashlib.md5(password).hexdigest()
        
        cursor = connections[DATABASE].cursor()
        
        # The query returns a result if and only if the given password mathces
        # the stored one; else no results are returned.
        query = """SELECT userid, username, email FROM {0}
                   WHERE username = %s
                   AND MD5(CONCAT(%s, salt)) = password""".format(TABLE_NAME)
        cursor.execute(query, [username, password])
        
        try:
            userid, username, email = cursor.fetchone()
        except TypeError:
            # No results returned, authentication failed
            return None
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
            user.is_staff = False
            user.is_superuser = False
            user.set_unusable_password()
            user.save()
            for g in GROUPS:
                user.groups.add(Group.objects.get(name=g))
        
        # Always update the email
        if user.email != email:
            user.email = email
            user.save()
        
        profile = user.get_profile()
        
        if profile.animedb_userid != userid:
            profile.animedb_userid = userid
            profile.save()
        
        return user
    


