from applications.shortcuts import render_to_response


def permission_required(request, *args, **kwargs):
    
    # @todo: Redirect to the login page if the user is not logged in.
    
    return render_to_response('auth/permissions.html', {
        'perm': kwargs.get('_perm', ''),
    }, request)
