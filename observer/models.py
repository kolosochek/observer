# -*- coding: utf-8 -*-
from django.db.models import Model, CharField, IntegerField, EmailField

class Ticket(Model):
    #def __init__(self):
    #    pass

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    #sphinx
    #unique_together = ('address', 'municipality')
    #db_table = 'adv'


    id = IntegerField(primary_key=True, unique=True, auto_created=True)
    ticket_id = IntegerField(verbose_name="Ticket number", unique=True, null=False)
    ticket_slug = CharField(max_length=30, verbose_name="Ticket slug", unique=True, null=False)
    ticket_subject = CharField(max_length=512, verbose_name= 'Ticket subject')
    ticket_department = CharField(max_length=64, verbose_name= 'Ticket department')
    ticket_status = CharField(max_length=64, verbose_name= 'Ticket status')
    ticket_activity = CharField(max_length=64, verbose_name= 'Ticket activity')
    ticket_due = CharField(max_length=64, verbose_name= 'Ticket due')
    ticket_owner = CharField(max_length=128, verbose_name= 'Ticket owner')
    ticket_replier = CharField(max_length=128, verbose_name= 'Ticket owner')
    ticket_email = CharField(max_length=256, verbose_name= 'Ticket email')
    ticket_priority = CharField(max_length=64, verbose_name= 'Ticket priotiry')

