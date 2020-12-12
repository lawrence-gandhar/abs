#
# AUTHOR : LAWRENCE GANDHAR
#
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from django.conf import settings
from app.models import *
from app.forms import *
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe

import json, imaplib, email


#******************************************************************************
# EMAIL MANAGEMENT CLASS
#******************************************************************************

class EmailManagement():

    def __init__(self):
        self.username = settings.EMAIL_HOST_USER
        self.passwd = settings.EMAIL_HOST_PASSWORD
        self.imap_url = 'imap.gmail.com'
        self.base_url = settings.BASE_URL
        self.reply_email = [settings.APPLICATION_EMAIL]
        self.app_email = settings.APPLICATION_EMAIL

        self.conn = imaplib.IMAP4_SSL(self.imap_url)
        self.conn.login(self.username, self.passwd)
        print(self.conn.list())


    #******************************************************************************
    # GET INBOX MESSAGE IDs
    #******************************************************************************
    def get_inbox_ids(self):
        self.conn.select('Inbox')

        status, msgs = self.conn.search(None, "ALL")

        ids = msgs[0].split()
        ids.reverse()
        return ids

    #******************************************************************************
    # GET SENT MAIL IDs
    #******************************************************************************
    def get_sent_ids(self):

        self.conn.select('"[Gmail]/Sent Mail"')

        status, msgs = self.conn.search(None, "ALL")

        ids = msgs[0].split()
        ids.reverse()
        return ids

    #******************************************************************************
    # SET MAIL LIMIT TO SHOW
    #******************************************************************************
    def mail_limit(self, ids = [], limit = None, start_index = None):

        limi_ids = []

        if limit is None:
            limit = 10


        if start_index is None:
            for i in range(limit):
                try:
                    limi_ids.append(ids[i])
                except:
                    pass
        else:
            for i in range(start_index, limit+start_index):
                try:
                    limi_ids.append(ids[i])
                except:
                    pass

        return limi_ids

    #******************************************************************************
    # FETCH INBOX ITEMS
    #******************************************************************************
    def inbox(self, get_all = True, limit = None, start_index = None):

        ids = self.get_inbox_ids()

        if not get_all:
            ids = self.mail_limit(ids, limit, start_index)

        mails_list = []

        for num in ids:
            data = self.fetch_mail_details(num)
            mails_list.append(data)

        return mails_list

    #******************************************************************************
    # FETCH SENT ITEMS
    #******************************************************************************
    def sentmail(self, get_all = True, limit = None, start_index = None):

        ids = self.get_sent_ids()

        if not get_all:
            ids = self.mail_limit(ids, limit, start_index)

        mails_list = []

        for num in ids:
            data = self.fetch_mail_details(num)
            mails_list.append(data)

        return mails_list


    #******************************************************************************
    # FETCH MAIL DETAILS
    #******************************************************************************
    def fetch_mail_details(self, num = None):

        typ, data = self.conn.fetch(num, '(RFC822)')

        mail_details = defaultdict()

        for response in data:

            if isinstance(response, tuple):

                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])

                # decode the email subject
                subject, encoding = email.header.decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)

                # decode email sender
                From, encoding = email.header.decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)

                # decode email sender
                To, encoding = email.header.decode_header(msg.get("To"))[0]
                if isinstance(From, bytes):
                    To = To.decode(encoding)

                # decode email sender
                Date, encoding = email.header.decode_header(msg.get("Date"))[0]
                if isinstance(From, bytes):
                    Date = Date.decode(encoding)

                index_st = From.find('<')
                From = From[:index_st]

                mail_details["msg_id"] = int(num)
                mail_details["subject"] = subject
                mail_details["from"] = From
                mail_details["mail_date"] = Date
                mail_details["mail_to"] = To

        return mail_details

    #******************************************************************************
    # FETCH MAIL BODY AND DETAILS
    #******************************************************************************
    def fetch_mail(self, mailbox = 'Inbox', num = None):

        #self.conn.login(self.username, self.passwd)
        self.conn.select('Inbox')
        status, msgs = self.conn.search(None, "ALL")

        mail_details = defaultdict()

        msgs = [int(num) for num in msgs[0].split()]

        if num in msgs:
            print(num)
            typ, data = self.conn.fetch(str(num), '(RFC822)')

            for response in data:

                if isinstance(response, tuple):

                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])

                    # decode the email subject
                    subject, encoding = email.header.decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)

                    # decode email sender
                    From, encoding = email.header.decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)

                    # decode email sender
                    Date, encoding = email.header.decode_header(msg.get("Date"))[0]
                    if isinstance(From, bytes):
                        Date = Date.decode(encoding)

                    mail_details["msg_id"] = int(num)
                    mail_details["subject"] = subject
                    mail_details["from"] = From
                    mail_details["mail_date"] = Date
                    mail_details["msg_body"] = []

                    # if the email message is multipart
                    if msg.is_multipart():

                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email

                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                # get the email body
                                msg_body = part.get_payload(decode=True).decode()

                                mail_details["msg_body"].append(mark_safe(msg_body))
                            except:
                                pass
                    else:
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                # get the email body
                                msg_body = part.get_payload(decode=True).decode()

                                mail_details["msg_body"].append(mark_safe(msg_body))
                            except:
                                pass
        return mail_details


    #******************************************************************************
    # SEND NEW MAIL
    #******************************************************************************
    def sendmail(self, email_html_template = None, data = None, reciever_email = []):
        email_html_template = get_template(email_html_template).render(data)
        email_msg = EmailMessage(msg_body, email_html_template, self.app_email, receiver_email, reply_to = self.reply_email)
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)



#******************************************************************************
# ADMIN EMAIL INBOX VIEW
#******************************************************************************

class AdminEmailInboxView(View):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/staff/email_management.html'

    data["page_title"] = "Email Management"

    data["css_files"] = ['custom_files/css/email.css']
    data["js_files"] = []

    #******************************************************************************
    #
    #******************************************************************************

    def get(self, request):

        email_cls = EmailManagement()
        msgs = email_cls.inbox(False)
        self.data["mails_list"] = msgs

        return render(request, self.template_name, self.data)

    #******************************************************************************
    #
    #******************************************************************************

    def post(self, request):
        pass



#******************************************************************************
# ADMIN EMAIL VIEW
#******************************************************************************

def inbox_email_view(request, msg_id = None):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/staff/inbox_email_view.html'

    data["page_title"] = "Email Management - Inbox"

    data["css_files"] = ['custom_files/css/email.css']
    data["js_files"] = []

    email_cls = EmailManagement()
    data["inbox_details"] = email_cls.inbox(False)
    data["msg_details"] = email_cls.fetch_mail('Inbox', msg_id)
    data["msg_id"] = msg_id

    return render(request, template_name, data)


#******************************************************************************
# ADMIN EMAIL SENT VIEW
#******************************************************************************

class AdminEmailSentView(View):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/staff/sent_mail.html'

    data["page_title"] = "Email Management - Sent Mails"

    data["css_files"] = ['custom_files/css/email.css']
    data["js_files"] = []

    #******************************************************************************
    #
    #******************************************************************************

    def get(self, request):

        email_cls = EmailManagement()
        msgs = email_cls.sentmail(False)
        self.data["mails_list"] = msgs

        return render(request, self.template_name, self.data)

    #******************************************************************************
    #
    #******************************************************************************

    def post(self, request):
        pass
