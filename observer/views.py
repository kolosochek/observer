# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout as logout_user
from django.shortcuts import HttpResponseRedirect, RequestContext, render_to_response, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Ticket, TicketForm

# Ticket list view
@staff_member_required
def tickets_view(request, page=1, per_page=10, ticket_department='', ticket_status='', filter_field='ticket_update_date', filter_order='desc'):
    # Build storage
    data = {
        'ticket_count': 0,
        'content': {},
        'paginator': '',
        'filter_field': filter_field,
        'filter_order': filter_order,
        'page': page,
        'page_1': page - 1,
        'page_2': page - 2,
        'page__1': page + 1,
        'page__2': page + 2,
        'per_page': per_page,
        'ticket_department': ticket_department,
        'ticket_status': ticket_status,
    }
    # page params
    page = request.GET.get('page', page)
    try:
        page = int(page)
    except ValueError:
        page = 1
    per_page = request.GET.get('per_page', per_page)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    # ticket params
    ticket_status = request.GET.get('ticket_status', data.get('ticket_status', ''))
    ticket_department = request.GET.get('ticket_department', data.get('ticket_department', ''))
    ticket_department = request.GET.get('ticket_department', '')
    ticket_department_filter = ''
    if ticket_department == '':
        ticket_department_filter = u'All'
    if ticket_department == 'support':
        ticket_department_filter = u'Техническая поддержка'
    if ticket_department == 'admin':
        ticket_department_filter = u'Дежурный администратор'
    if ticket_department == 'director':
        ticket_department_filter = u'Руководство'
    if ticket_department == 'finance':
        ticket_department_filter = u'Фин.отдел'
    if ticket_department == 'abuse':
        ticket_department_filter = u'Жалобы'
    if ticket_department == 'superadmin':
        ticket_department_filter = u'Старший администратор'
    ticket_status_filter = ticket_status.title()
    filter_expression = ''
    if filter_order == 'desc':
        filter_expression = '-'
    elif filter_order == 'asc':
        pass
    else:
        ''
    filter_expression += filter_field
    # filter params
    filter_field = request.GET.get('filter_field', data.get('filter_field', 'ticket_id'))
    filter_order = request.GET.get('filter_order', data.get('filter_order', 'desc'))

    # Ticket_deparment does not set
    if not ticket_department:
        try:
            open_ticket_count = Ticket.objects.filter(ticket_status=ticket_status_filter).count()
        except Exception:
            open_ticket_count = 0
        # Ticket status doesn't set
        if not ticket_status:
            content = Ticket.objects.order_by(filter_expression)
        # Got ticket status
        else:
            content = get_list_or_404(Ticket.objects.order_by(filter_expression), ticket_status=ticket_status_filter)
    # Got ticket_deparment
    else:
        # open tickets by department count(open_ticket_count)
        try:
            open_ticket_count = len(get_list_or_404(Ticket, ticket_department=request.user.get_department(), ticket_status="Open"))
        except Exception:
            open_ticket_count = 0

        # No ticket status
        if not ticket_status:
            content = Ticket.objects.order_by(filter_expression)
        # Got ticket status
        if not ticket_status:
            content = get_list_or_404(Ticket.objects.order_by(filter_expression), ticket_department=ticket_department_filter)
        else:
            content = get_list_or_404(Ticket.objects.order_by(filter_expression), ticket_status=ticket_status_filter, ticket_department=ticket_department_filter)

    ticket_count = len(content)
    paginator = Paginator(object_list=content, per_page=per_page)
    data = {'page': page,
            'page_1': page - 1,
            'page_2': page - 2,
            'page__1': page + 1,
            'page__2': page + 2,
            'per_page': per_page,
            'ticket_department': ticket_department,
            'ticket_status': ticket_status,
            'ticket_status_filter': ticket_status_filter,
            'ticket_count': ticket_count,
            'page_range': paginator.page_range
            }
    try:
        content = paginator.page(page)
    # If page is not an integer, just return first page
    except PageNotAnInteger:
        paginator = Paginator(object_list=content, per_page=per_page)
        content = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        paginator = Paginator(object_list=content, per_page=per_page)
        content = paginator.page(paginator.num_pages)
    # Build pagination labels
    # results from
    try:
        results_from = 1 if page not in data.get('page_range', [1]) or data.get('page', 1) == 1 else data.get('page_1', 1) * data.get('per_page', 10) + 1
    except ValueError:
        results_from = 1
    if data.get('ticket_count', 0) < results_from:
        results_from = data.get('ticket_count', 0)
    # Results to
    try:
        results_to = 1 if page not in data.get('page_range', [1]) else data.get('page_1', 1) * data.get('per_page', 10) + data.get('per_page', 10)
    except ValueError:
        results_to = 1
    # First page
    if page == 1:
        results_from = 1
        results_to = page * data.get('per_page', 10) if data.get('ticket_count', 0) > page * data.get('per_page', 10) else data.get('ticket_count', 0)
    # Last_page
    if data.get('page_range', False):
        page_range = data.get('page_range', [])
        last_page = int(page_range[-1])
        if page == last_page:
            if results_from != 1:
                results_from = data.get('page_1', 1) * data.get('per_page', 10)
            results_to = results_from + data.get('per_page', 10) if results_from + data.get('per_page', 10) < data.get('ticket_count', 0) else data.get('ticket_count', 0)
    else:
        last_page = 1
    # Save data to storage
    data['last_page'] = last_page
    data['ticket_department'] = ticket_department
    data['ticket_status'] = ticket_status
    data['ticket_count'] = ticket_count
    data['results_from'] = results_from
    data['results_to'] = results_to
    data['filter_field'] = filter_field
    data['filter_order'] = filter_order
    data['open_ticket_count'] = open_ticket_count
    # debug
    data['debug'] = request.user
    # render results
    return render_to_response('ticket_list.html', {"content": content, "ticket_count": ticket_count, 'paginator': paginator, 'data': data }, context_instance=RequestContext(request))

# Ticket searh view
@staff_member_required
def search(request, query='', page=1, per_page=10, ticket_department='', ticket_status='', filter_field='ticket_id', filter_order='desc'):
    query = request.GET.get('query', query)
    filter_field = request.GET.get('filter_field', filter_field)
    page = request.GET.get('page', page)
    per_page = request.GET.get('per_page', per_page)
    filter_order = request.GET.get('filter_order', filter_order)
    # Collect all info into data dict
    data = {
        'query': query,
        'ticket_count': 0,
        'content': {},
        'paginator': '',
        'page': page,
        'per_page': per_page,
        'filter_field': filter_field,
        'filter_order': filter_order,
        'ticket_department': ticket_department,
        'ticket_status': ticket_status,
        }
    # Create QuerySet and search for
    ### At the first time search by ticket_subject
    content = get_list_or_404(Ticket, ticket_subject__icontains=data.get('query', query.lower()))

    ### Then, if nothing found, search by ticket_slug
    if not len(content):
        content = get_list_or_404(Ticket, ticket_slug__icontains=data.get('query', query.lower()))

    ### If still got no result, search by ticket_id
    if not len(content):
        if query:
            try:
                query = int(query)
            except ValueError:
                pass
            content = get_list_or_404(Ticket, ticket_id__icontains=query)
    return render_to_response('ticket_list.html', {"content": content, 'data': data}, context_instance=RequestContext(request))

# Detail ticket view
@staff_member_required
def detail_view(request, ticket_id=False):
    data = {}
    ticket_id = request.GET.get('ticket_id', ticket_id)
    try:
        ticket_id = int(ticket_id)
    except ValueError:
        ticket_id = 0
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    form = TicketForm()

    # Update values
    if request.method == 'POST':
        ticket.ticket_status = request.POST.get('ticket_status', False)
        ticket.ticket_department = request.POST.get("ticket_department", False)
        ticket.ticket_update_date = datetime.now()
        # Try to save ticket
        try:
            ticket.save()
            return render_to_response('ticket_detail.html', {"content": ticket, 'form': form, 'data': data}, context_instance=RequestContext(request))
        except Exception:
            print("Can't save a ticket!")
    # View values
    else:
        if ticket_id:
            data = {
                'ticket_id': ticket_id,
                'ticket': {},
                }
            return render_to_response('ticket_detail.html', {"content": ticket, 'form': form, 'data': data}, context_instance=RequestContext(request))

# User profile page view
@staff_member_required
def profile(request):
    data = {}
    user = request.get('user', False)
    if user:
        return render_to_response('profile', {"content": user, 'data': data}, context_instance=RequestContext(request))
    else:
        pass

# Logout view
def logout(request):
    logout_user(request)
    return HttpResponseRedirect('/')

# Custom error handlers
# 404
def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response
# 500
def handler500(request):
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response