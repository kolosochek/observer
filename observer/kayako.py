# -*- coding: utf-8 -*-
# -*- author kolosochek@gmail.com -*- #
from observer.models import Ticket
from grab import Grab, GrabError

class Kayako:
    grab = Grab()
    is_authorized = False

    # increase perfomance
    limit_results = 15 #False
    include_last_message = False # True

    # credentials
    # put your
    username = "Vasya"
    password = "Pupkin"


    # url
    url = "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=manage&departmentid=1&ticketstatusid=1"
    # Техническая поддержка department
    department_url = "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=manage&departmentid=1&ticketstatusid=3"
    department_url_closed = "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=manage&departmentid=1&ticketstatusid=3"

    # ticket
    ticket_list_selector = "#ticketlist td.contenttableborder tr[id!=''][id!='trmassaction']"
    ticket_last_message_selector = "td.contenttableborder td.ticketrow1:last .mediumtext"
    ticket_id_prefix = "trid"

    # kayako encoding
    encoding = "koi8-r"


    def __init__(self):
        if not self.is_authorized:
            self.do_authorize()

    # safe url open
    def safe_go(self, url):
        if url:
            try:
                self.grab.go(url)
                if self.grab.response.code == 200:
                    pass
                else:
                    # repeat request until get HTTP 200
                    self.grab.go(url)
            except GrabError as error:
                # repeat request
                print("Got network error %s, repeating request" % error)
                self.safe_go(url)
        else:
            raise BaseException("Can't safe_go, url is empty")

    def do_authorize(self):
        if not self.is_authorized:
            try:
                self.safe_go(self.url)
            except:
                raise BaseException("Can't get kayako page")
            if u"Tickets List" in self.grab.response.body.decode(self.encoding):
                # set autorization flag
                self.is_authorized = True
            else:
                # fill authorization form
                if self.grab.doc.pyquery.find("#username").length:
                    self.grab.doc.set_input_by_id('username', self.username)
                    self.grab.doc.set_input_by_id('password', self.password)
                    self.grab.doc.submit()
                    #if u"Tickets List:" in self.grab.response.body.decode(self.encoding):
                    self.is_authorized = True
                    #else:
                    #    raise BaseException("Can't find login string in loaded page")
                else:
                    if u"Tickets List" in self.grab.response.body.decode(self.encoding):
                        self.is_authorized = True
                    else:
                        self.grab.response.browse()
                        raise BaseException("Can't find login string in loaded page")


    def get_ticket_by_id(self, ticket_id, content_type='html'):
        if ticket_id:
            ticket_url = "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=viewticket&ticketid=%s" % ticket_id
            self.grab.go(ticket_url)
            data = self.grab.doc.pyquery(self.grab.response.body.decode(self.encoding))
            # debug
            self.last_ticket_message = data.find(self.ticket_last_message_selector)
            self.last_ticket_message_id = ticket_id
            #
            #last_ticket_message = data.find(self.ticket_last_message_selector).text()
            last_ticket_message = data.find(self.ticket_last_message_selector)[0].text_content()
            if content_type == "html":
                return last_ticket_message
            else:
                last_ticket_message = {'last_message': data.find(self.ticket_last_message_selector)[0].text_content()}
                return last_ticket_message
        else:
            raise("Got no ticket_id")

    def get_ticket_list(self, url='&departmentid=1&ticketstatusid=1', mode='short', content_type='json'):
        def parse_ticket_list(index, node):
            if not node.attrib.get('id', False) == "trmassaction":
                # store ticket_id
                ticket_id = node.attrib.get('id', False)
                # make sure that we are working with ticket tr node
                ticket_id = ticket_id.replace(self.ticket_id_prefix, '') \
                    if self.ticket_id_prefix in ticket_id and ticket_id != "trmassaction" \
                    else False
                if ticket_id: #and self.ticket_id_prefix in ticket_id:
                    node = self.grab.doc.pyquery(node)
                    # parse ticket info
                    ticket_slug = node.find("td[align='center'][width='80']").eq(0).text()
                    ticket_subject = node.find("td[align='left']").text()
                    ticket_department = node.find("td[align='center'][width='120']").text()
                    if u"техническая" in ticket_department.lower():
                        ticket_department = u"Техническая поддержка"
                    elif u"дежурный" in ticket_department.lower():
                        ticket_department = u"Дежурный администратор"
                    elif u"руковод" in ticket_department.lower():
                        ticket_department = u"Руководство"
                    elif u"старши" in ticket_department.lower():
                        ticket_department = u"Старший Администратор"
                    ticket_status = node.find("td[align='center'][width='100']").eq(0).text()
                    ticket_activity = node.find("td[align='center'][width='100']").eq(1).text()
                    ticket_due = node.find("td[align='center'][width='80']").eq(1).text()
                    ticket_owner = node.find("td[align='center'][width='130']").eq(0).text()
                    if u"unassigned" in ticket_owner.lower():
                        ticket_owner = False
                    ticket_email = node.find("td[align='center'][width='180']").text()
                    ticket_replier = node.find("td[align='center'][width='130']").eq(1).text()
                    ticket_priority = node.find("td[align='center'][width='90']").text()
                    ticket_last_message = self.get_ticket_by_id(ticket_id) if self.include_last_message else ''
                    self.ticket_count+=1
                    # and store it into dict
                    self.ticket_list_dict['ticket_%s' % (index)] = {
                        "ticket_id": ticket_id,
                        "ticket_slug": ticket_slug,
                        "ticket_subject": ticket_subject,
                        "ticket_department": ticket_department,
                        "ticket_status": ticket_status,
                        "ticket_activity": ticket_activity,
                        "ticket_due": ticket_due,
                        "ticket_owner": ticket_owner,
                        "ticket_email": ticket_email,
                        "ticket_replier": ticket_replier,
                        "ticket_priority": ticket_priority,
                        "ticket_last_message": ticket_last_message
                    }
                    try:
                        ticket_to_update = Ticket.objects.filter(ticket_id=ticket_id).first()
                        print "Ticket # %s already exist" % ticket_id
                    except Ticket.DoesNotExist:
                        ticket_to_update = False
                        print "Can't find an object"
                    #
                    if ticket_to_update:
                        ticket_to_update.ticket_id = ticket_id
                        ticket_to_update.ticket_slug = ticket_slug
                        ticket_to_update.ticket_subject = ticket_subject
                        ticket_to_update.ticket_department = ticket_department
                        ticket_to_update.ticket_status = ticket_status
                        ticket_to_update.ticket_activity = ticket_activity
                        ticket_to_update.ticket_due = ticket_due
                        ticket_to_update.ticket_owner = ticket_owner
                        ticket_to_update.ticket_email = ticket_email
                        ticket_to_update.ticket_replier = ticket_replier
                        ticket_to_update.ticket_priority = ticket_priority
                        ticket_to_update.ticket_last_message = ticket_last_message
                        # save changed fields to db
                        try:
                            ticket_to_update.save()
                            print "Ticked # %s updated" % ticket_id
                            print "Ticket slug %s status %s" % (ticket_slug, ticket_status)
                        except Exception:
                            print "Can't update ticket # %s" % ticket_id
                    else:
                        # create ticket object
                        try:
                            ticket, created = Ticket.objects.get_or_create(ticket_id = ticket_id, ticket_slug= ticket_slug, ticket_subject= ticket_subject,
                                            ticket_department= ticket_department,ticket_status= ticket_status,
                                            ticket_activity= ticket_activity, ticket_due= ticket_due,
                                            ticket_owner= ticket_owner, ticket_email= ticket_email,
                                            ticket_last_message= ticket_last_message )
                            try:
                                ticket.save()
                                print "Ticket %s" % created
                            except Exception:
                                print('Oops something broke down')
                        except Ticket.DoesNotExist:
                            print("Can't create new ticket, maybe ticket already exist?")

        base_url = "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=manage"
        url = "%s%s" % (base_url, url)
        if mode == 'short':
            self.include_last_message = False
        elif mode == 'detail':
            self.include_last_message = True
        if url:
            self.safe_go(url)
            data = self.grab.doc.pyquery(self.grab.response.body.decode(self.encoding))
            self.data = data
            self.ticket_list = data.find(self.ticket_list_selector)
            self.ticket_list_dict = {}
            self.ticket_count = 0
            self.ticket_list.each(parse_ticket_list)
            return self.ticket_list_dict
        else:
            raise("Got no ticket_list url")

    def get_ticket_dict(self, url='&departmentid=1&ticketstatusid=1', mode='short', content_type='json'):
        def parse_ticket_list(index, node):
            # store ticket_id
            ticket_id = node.attrib.get('id', False)
            # make sure that we are working with ticket tr node
            ticket_id = ticket_id.replace(self.ticket_id_prefix, '') \
                if self.ticket_id_prefix in ticket_id and ticket_id != "trmassaction" \
                else False
            #print ticket_id
            if ticket_id: #and self.ticket_id_prefix in ticket_id:
                node = self.grab.doc.pyquery(node)
                # parse ticket info
                ticket_slug = node.find("td[align='center'][width='80']").eq(0).text()
                ticket_subject = node.find("td[align='left']").text()
                ticket_department = node.find("td[align='center'][width='120']").text()
                if u"техническая" in ticket_department.lower():
                    ticket_department = u"Техническая поддержка"
                elif u"дежурный" in ticket_department.lower():
                    ticket_department = u"Дежурный администратор"
                elif u"руковод" in ticket_department.lower():
                    ticket_department = u"Руководство"
                elif u"старши" in ticket_department.lower():
                    ticket_department = u"Старший Администратор"
                ticket_status = node.find("td[align='center'][width='100']").eq(0).text()
                ticket_activity = node.find("td[align='center'][width='100']").eq(1).text()
                ticket_due = node.find("td[align='center'][width='80']").eq(1).text()
                ticket_owner = node.find("td[align='center'][width='130']").eq(0).text()
                if u"unassigned" in ticket_owner.lower():
                    ticket_owner = False
                ticket_email = node.find("td[align='center'][width='180']").text()
                ticket_replier = node.find("td[align='center'][width='130']").eq(1).text()
                ticket_priority = node.find("td[align='center'][width='90']").text()
                ticket_last_message = self.get_ticket_by_id(ticket_id) if self.include_last_message else ''
                self.ticket_count+=1
                # and store it into dict
                self.ticket_list_dict['ticket_%s' % (index)] = {
                    "ticket_id": ticket_id,
                    "ticket_slug": ticket_slug,
                    "ticket_subject": ticket_subject,
                    "ticket_department": ticket_department,
                    "ticket_status": ticket_status,
                    "ticket_activity": ticket_activity,
                    "ticket_due": ticket_due,
                    "ticket_owner": ticket_owner,
                    "ticket_email": ticket_email,
                    "ticket_replier": ticket_replier,
                    "ticket_priority": ticket_priority,
                    "ticket_last_message": ticket_last_message
                }
                # create ticket object
                #ticket = Ticket(ticket_id = ticket_id, ticket_slug= ticket_slug, ticket_subject= ticket_subject,
                #                ticket_department= ticket_department,ticket_status= ticket_status,
                #                ticket_activity= ticket_activity, ticket_due= ticket_due,
                #                ticket_owner= ticket_owner, ticket_email= ticket_email,
                #                ticket_replier= ticket_replier, ticket_priority= ticket_priority)
                #ticket_last_message= ticket_last_message )
                #self.ticket = ticket
                #ticket.save()
                #if not ticket[1]:
                #    pass
                #    ticket.save()
                #else:
                #    ticket = ticket[0]
        base_url = "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=manage"
        url = "%s%s" % (base_url, url)
        if mode == 'short':
            self.include_last_message = False
        elif mode == 'detail':
            self.include_last_message = True
        if url:
            self.safe_go(url)
            data = self.grab.doc.pyquery(self.grab.response.body.decode(self.encoding))
            self.data = data
            self.ticket_list = data.find(self.ticket_list_selector)
            self.ticket_list_dict = {}
            self.ticket_count = len(self.ticket_list)
            self.ticket_list.each(parse_ticket_list)
            #print self.ticket_list_dict
            self.ticket_list_dict['ticket_count'] = self.ticket_count
            return self.ticket_list_dict
        else:
            raise("Got no ticket_list url")

    def get_tickets(self, pagenumber=1, limit=50):
        pass



