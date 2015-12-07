# -*- coding: utf-8 -*-
from django.shortcuts import render, RequestContext, render_to_response, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.core.paginator import EmptyPage
from django.http import HttpResponseRedirect
from kayako import Kayako
from django.template import Context, Template
from models import Ticket
from django.http import JsonResponse

# create kayako class object
kayako = Kayako()
# get some tickets
#kayako.do_authorize()

def tickets_view(request, url="&departmentid=1&ticketstatusid=1", mode='short', content_type='html'):
    if request.user.is_authenticated():
        if content_type == 'html':
            content = kayako.get_ticket_list(url=url, mode=mode, content_type=content_type)
            ticket_count = kayako.ticket_count
            return render_to_response('ticket_list.html', {"content": content, "ticket_count": ticket_count}, context_instance=RequestContext(request))
        elif content_type == 'json':
            content = kayako.get_ticket_list(url=url, mode=mode, content_type=content_type)
            content['ticket_count'] = len(content.items())
            return JsonResponse(content)
        else:
            return redirect('/tickets/login/')
    else:
        return redirect('/tickets/login/')

def logout(request):
    return redirect('/tickets/logout/')