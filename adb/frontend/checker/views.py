# -*- coding: utf-8 -*-

import urlparse

from django.db import connections
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from adb.frontend.auth.decorators import permission_required, checks_permissions, require_permissions
from adb.frontend.shortcuts import render_to_response

from adb.frontend.checker import forms

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
    
    query = """SELECT p.pagetext, u.username, u.userid, t.title
               FROM thread t
               INNER JOIN post p ON t.firstpostid = p.postid
               INNER JOIN user u ON t.postuserid = u.userid
               WHERE t.threadid=%s AND t.forumid=%s"""
    
    cursor.execute(query, [int(release), FORUM])
    
    try:
        content, poster, posterid, title = cursor.fetchone()
    except TypeError:
        # No results returned, invalid ID or topic not in the allowed forum
        messages.error(request, 'Topic non trovato, assicurati che il topic esista e si trovi nel forum “Streaming › Film.”')
        return redirect('checker:index')
    
    from parser import PostParser
    from jinja2.utils import escape
    
    parser = PostParser()
    result, normalized, uppers = parser.parse(content)
    
    users = [[posterid, poster, 'Autore', [(posterid, poster)], 0]]
    
    offset = 0
    
    def mark(text, count, open, close, offset=0):
        start = '$$%d$$' % count
        end = '$$/%d$$' % count 
        
        text = text[:open + offset] + start + text[open + offset:]
        offset += len(start)
        text = text[:close + offset] + end + text[close + offset:]
        offset += len(end)
        
        return text, offset
    
    for i, upper in enumerate(uppers):
        content, offset = mark(content, i, upper[1], upper[2], offset)
        db_users = None
        query = """SELECT userid, username
                   FROM user
                   WHERE username=%s"""
        
        cursor.execute(query, [upper[0]])
        try:
            db_users = cursor.fetchall()
            
            if not db_users:
                raise TypeError
        except TypeError:
            try:
                query = """SELECT userid, username
                           FROM user
                           WHERE username LIKE %s"""
                
                cursor.execute(query, ['%' + upper[0] + '%'])
                db_users = cursor.fetchall()
                
                if not db_users:
                    raise TypeError
            except TypeError:
                # No results returned, invalid username
                users.append((None, upper[0], 'Testo', [(None, u'—')], i))
        
        if db_users:
            if len(db_users) is 1:
                userid = db_users[0][0]
            else:
                userid = None
            username = db_users
            
            if users[0][0] == userid:
                if not users[0][2].endswith('e testo'):
                    users[0][2] += ' e testo'
            else:
                users.append((userid, upper[0], 'Testo', username, i))
    
    content = unicode(escape(content))
    
    for i, upper in enumerate(uppers):
        content = content.replace('$$%d$$' % i, '<span id="U%d"> ' % i)
        content = content.replace('$$/%d$$' % i, '</span>')
    
    return render_to_response('checker/results.html', {
        'release': release,
        'content': content,
        'uppers': users,
        'urls': normalized,
        'images': result['Immagine'],
        'title': title,
    }, request)

