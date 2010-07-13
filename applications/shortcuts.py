# -*- coding: utf-8 -*-
from coffin import shortcuts

from django.template import RequestContext
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives

def render_to_string(template, context={}, request=None):
    if request:
        context_instance = RequestContext(request)
    else:
        context_instance = None
    return shortcuts.render_to_string(template, context, context_instance)
 
def render_to_response(template, context={}, request=None, mimetype="text/html"):
    response = render_to_string(template, context, request)
    return HttpResponse(response, mimetype=mimetype)

def render_to_mail(subject, sender, recipients, text_template, html_template, context, request=None):
    text_message = render_to_string(text_template, context, request)
    mail = EmailMultiAlternatives(subject, text_message, sender, recipients)
    
    if html_template:
        html_message = render_to_string(html_template, context, request)
        mail.attach_alternative(html_message, "text/html")
        
    mail.send()