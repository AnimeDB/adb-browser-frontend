# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db import IntegrityError
from shortcuts import render_to_response

from applications.lists.models import List
from applications.lists.forms import ListForm

@permission_required('lists.view_list')
def view(request, id):
    l = get_object_or_404(List, pk=id, user=request.user)
    
    return render_to_response('lists/view.html', {
        'list': l,
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

@permission_required('lists.add_list')
def edit(request, id=None):
    if id is not None:
        instance = get_object_or_404(List, pk=id, user=request.user)
    else:
        instance = List(user=request.user)
    
    if request.method == 'POST':
        form = ListForm(request.POST, instance=instance)
        
        if form.is_valid():
            try:
                l = form.save()
                
                if id is None:
                    msg = u"La lista “%s” é stata correttamete creata."
                else:
                    msg = u"La lista “%s” é stata correttamete rinominata."
                
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
