from adb.frontend.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def permission_required(request, *args, **kwargs):
    
    # @todo: Redirect to the login page if the user is not logged in.
    
    return render_to_response('auth/permissions.html', {
        'perm': kwargs.get('_perm', ''),
    }, request)
