# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Model, CharField, OneToOneField, IntegerField, BooleanField, EmailField, TextField, DateTimeField, ForeignKey
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import widgets

DEPARTMENT_CHOICES = (
    ('', 'All'),
    ('Техническая поддержка', 'Техническая поддержка'),
    ('Дежурный администратор', 'Дежурный администратор'),
    ('Руководство', 'Руководство'),
    ('Фин.отдел', 'Фин.отдел'),
    ('Жалобы', 'Жалобы'),
    ('Старший администратор', 'Старший администратор'),
)
#
STATUS_CHOICES = (
    ('', 'All'),
    ('Open', 'Open'),
    ('Closed', 'Closed'),
    ('Hold', 'Hold'),
)
#
PRIORITY_CHOICES = (
    ('', 'All'),
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)

# Extend base user
class Employee(Model):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

    user = OneToOneField(User)
    department = CharField(max_length=100)

    def get_department(self):
        return self.department

    def __str__(self):
        return "%s" % self.user

    def __unicode__(self):
        return "%s" % self.user


# Ticket(request, client, whatever)
class Ticket(Model):
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
    #
    id = IntegerField(primary_key=True, unique=True, auto_created=True)
    ticket_id = IntegerField(verbose_name="Ticket number", unique=True, null=False)
    ticket_slug = CharField(max_length=30, verbose_name="Ticket slug", unique=True, null=False)
    ticket_subject = CharField(max_length=512, verbose_name= 'Ticket subject')
    ticket_department = CharField(max_length=64, verbose_name= 'Ticket department', choices=DEPARTMENT_CHOICES, default='All', blank=True)
    ticket_status = CharField(max_length=64, verbose_name= 'Ticket status', choices=STATUS_CHOICES, default='All', blank=True)
    ticket_activity = CharField(max_length=64, verbose_name= 'Ticket activity')
    ticket_due = CharField(max_length=64, verbose_name= 'Ticket due', blank=True)
    ticket_owner = CharField(max_length=128, verbose_name= 'Ticket owner', blank=True)
    ticket_replier = CharField(max_length=128, verbose_name= 'Ticket owner', blank=True)
    ticket_email = CharField(max_length=256, verbose_name= 'Ticket email', blank=True)
    ticket_priority = CharField(max_length=64, verbose_name= 'Ticket priority', choices=PRIORITY_CHOICES, default='All', blank=True)
    ticket_last_message = TextField(max_length=8096, verbose_name= 'Ticket email', blank=True)
    ticket_update_date = DateTimeField(default=datetime.now(), blank=True)

    def get_id(self):
        return self.id

    def get_ticket_id(self):
        return self.ticket_id

    def update_date(self):
        self.ticket_update_date = datetime.now()

    def __str__(self):
        return "%s %s" % (self.ticket_slug, self.ticket_subject)

    def __unicode__(self):
        return "%s %s" % (self.ticket_slug, self.ticket_subject)

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_department', 'ticket_status', ]
        widgets = {
            #'ticket_subject': widgets.Textarea(attrs={'class': 'b-textarea b-input b-input-ticket-subject form-control col-lg-12', 'rows': '2', 'placeholder': ''}),
            'ticket_status': widgets.Select(attrs={'class': 'b-select form-control '}),
            'ticket_department': widgets.Select(attrs={'class': 'b-select form-control '})
        }
