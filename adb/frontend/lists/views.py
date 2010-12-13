# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from adb.frontend.auth.decorators import permission_required, checks_permissions, require_permissions
from adb.frontend.lists.forms import ListForm
from adb.frontend.lists.models import List
from adb.frontend.shortcuts import render_to_response


@permission_required('lists.browse_lists')
def index(request):
    return render_to_response('lists/index.html', {
        'lists': request.user.list_set.all(),
    }, request)


@permission_required('lists.view_list')
def view(request, id):
    l = get_object_or_404(List, pk=id, user=request.user)
    
    return render_to_response('lists/view.html', {
        'list': l,
        'items': l.movies.all(),
    }, request)


@permission_required('lists.delete_list')
def delete(request, id):
    l = get_object_or_404(List, pk=id, user=request.user)
    
    if request.method == 'POST':
        l.delete()
        messages.success(request, u"La lista “%s” é stata correttamete eliminata." % l.name)
        return redirect('index')
    
    return render_to_response('lists/confirm.html', {
        'list': l,
    }, request)


@checks_permissions
def edit(request, id=None):
    if id is not None:
        require_permissions(request.user, 'lists.change_list')
        instance = get_object_or_404(List, pk=id, user=request.user)
    else:
        require_permissions(request.user, 'lists.add_list')
        instance = List(user=request.user)
    
    if request.method == 'POST':
        form = ListForm(request.POST, instance=instance)
        
        if form.is_valid():
            try:
                l = form.save()
                
                if id is None:
                    msg = u"La lista “%s” é stata creata correttamete."
                else:
                    msg = u"La lista “%s” é stata rinominata correttamete."
                
                messages.success(request, msg % l.name)
                return redirect(l)
            except IntegrityError:
                form._errors = {
                    'name': form.error_class([u'Non è possibile usare lo stesso nome per più liste'])
                }
    else:
        form = ListForm(instance=instance)
    
    return render_to_response('lists/edit.html', {
        'form': form,
        'instance': instance,
        'editing': id is not None,
    }, request)

