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
    
    print "Start"
    
    cursor = connections[DATABASE].cursor()
    
    query = """SELECT p.pagetext, u.username, u.userid, t.title
               FROM thread t
               INNER JOIN post p ON t.firstpostid = p.postid
               INNER JOIN user u ON t.postuserid = u.userid
               WHERE t.threadid=%s AND t.forumid=%s"""
    
    cursor.execute(query, [int(release), FORUM])
    
    try:
        content, poster, posterid, title = cursor.fetchone()
        print "End"
    except TypeError:
        # No results returned, invalid ID or topic not in the allowed forum
        messages.error(request, 'Topic non trovato, assicurati che il topic esista e si trovi nel forum “Streaming › Film.”')
        return redirect('checker:index')
    
    from parser import PostParser
    from jinja2.utils import escape
    
    parser = PostParser()
    result, normalized, uppers = parser.parse(content)
    
    users = [[posterid, poster, 'Autore']]
    
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
        
        query = """SELECT userid, username
                   FROM user
                   WHERE username LIKE %s"""
        
        cursor.execute(query, ['%' + upper[0] + '%'])
        try:
            userid, username = cursor.fetchone()
        except TypeError:
            # No results returned, invalid username
            users.append((None, upper[0], 'Testo', 'Non trovato', i))
        else:
            if users[0][0] == userid:
                if not users[0][2].endswith('e testo'):
                    users[0][2] += ' e testo'
                    users[0].append(username)
                    users[0].append(i)
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

