# -*- coding: utf-8 -*-

import urlparse

from django.db import connections
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from applications.auth.decorators import permission_required, checks_permissions, require_permissions
from applications.shortcuts import render_to_response

from applications.checker import forms

#@permission_required('checker.i')
def index(request):
    
    if request.method == 'POST':
        form = forms.CheckForm(request.POST)
        
        if form.is_valid():
            return redirect('checker:check', release=form.cleaned_data['id'])
    else:
        form = forms.CheckForm()
    
    return render_to_response('checker/index.html', {
        'form': form,
    }, request)

def check(request, release):
    
    DATABASE = 'forum'
    FORUM = 18
    
    cursor = connections[DATABASE].cursor()
    
    query = """SELECT p.pagetext
               FROM thread t INNER JOIN post p ON t.firstpostid = p.postid
               WHERE t.threadid=%s AND t.forumid=%s"""
    
    cursor.execute(query, [int(release), FORUM])
    
    try:
        content, = cursor.fetchone()
    except TypeError:
        # No results returned, invalid ID or topic not in the allowed forum
        messages.error(request, 'Topic non trovato, assicurati che il topic esista e si trovi nel forum “Streaming › Film.”')
        return redirect('checker:index')
    
    return render_to_response('checker/results.html', {
        'release': release,
        'content': content,
    }, request)