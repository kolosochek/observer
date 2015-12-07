# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from models import *
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group

class TicketAdmin(ModelAdmin):
    #resource_class = AdResource
    suit_classes = 'suit-tab suit-tab-ad'
    list_display = ['ticket_id', 'ticket_slug', 'ticket_subject', 'ticket_department', 'ticket_status']
    fieldsets = [
        ('Basic information', {
            'description': 'Basic information',
            'classes': ('suit-tab', 'suit-tab-basic'),
            'fields': ['ticket_id', 'ticket_slug', 'ticket_subject']
        }),
        ('Additional information', {
            'description': 'Additional information',
            'classes': ('suit-tab', 'suit-tab-description'),
            'fields': ['ticket_department', 'ticket_status',]
        }),
    ]
    suit_form_tabs = (('basic', 'Basic information'),
                      ('description', 'Additional information'),)

admin.site.register(Ticket, TicketAdmin)
#admin.site.unregister(User)
admin.site.unregister(Group)