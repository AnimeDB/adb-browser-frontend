

class PermissionRequired(Exception):
    """
    Exception to be thrown by views which check permissions internally.
    Takes a single C{perm} argument which defines the permission that caused
    the exception.
    """
    def __init__(self, perm):
        self.perm = perm


def require_permissions(user, *permissions):
    for perm in permissions:
        if not user.has_perm(perm):
            raise PermissionRequired(perm)


class checks_permissions(object):
    """
    Decorator for views which handle C{PermissionRequired} errors and renders
    the given error view if necessary.
    The original request and arguments are passed to the error with the 
    additional C{_perm} and C{_view} keyword arguments.
    """
    def __init__(self, view_or_error=None):
        self.wrapped = callable(view_or_error)
        error_view = None
        
        if self.wrapped:
            self.view = view_or_error
        else:
            error_view = view_or_error
        
        if not error_view:
            from django.conf import settings
            error_view = settings.PERMISSIONS_VIEW
        
        from django.core.urlresolvers import get_callable
        self.error_view = get_callable(error_view)
    
    def __call__(self, view_or_request, *args, **kwargs):
        if not self.wrapped:
            self.view = view_or_request
        
        def dec(*args, **kwargs):
            try:
                return self.view(*args, **kwargs)
            except PermissionRequired as e:
                kwargs['_perm'] = e.perm
                kwargs['_view'] = self.view
                return self.error_view(*args, **kwargs)
        
        return dec(view_or_request, *args, **kwargs) if self.wrapped else dec


class permission_required(object):
    """
    Decorator which builds upon the C{checks_permission} decorator to offer
    the same functionality as the built-in
    C{django.contrib.auth.decorators.permission_required} decorator but which
    renders an error view insted of redirecting to the login page.
    """
    def __init__(self, perm, error_view=None):
        self.perm = perm
        self.error_view = error_view
    
    def __call__(self, view_func):
        def decorator(request, *args, **kwargs):
            if not request.user.has_perm(self.perm):
                raise PermissionRequired(self.perm)
            return view_func(request, *args, **kwargs)
        return checks_permissions(self.error_view)(decorator)


