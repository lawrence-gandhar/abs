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

import json, imaplib, email


#******************************************************************************
# EMAIL MANAGEMENT
#******************************************************************************

class EmailManagement():

    def __init__(self):
        self.username = settings.EMAIL_HOST_USER
        self.passwd = settings.EMAIL_HOST_PASSWORD
        self.imap_url = 'imap.gmail.com'
        self.conn = None
        self.base_url = settings.BASE_URL
        self.reply_email = [settings.APPLICATION_EMAIL]
        self.app_email = settings.APPLICATION_EMAIL

    #
    #
    #
    def connect(self):
        self.conn = imaplib.IMAP4_SSL(self.imap_url)
        self.conn.login(self.username, self.passwd)

    #
    #
    #
    def inbox(self):
        self.conn.select('Inbox')
        result, mails = con.search(None, key, '"{}"'.format(value))

        msgs = [] # all the email data are pushed inside an array
        for num in mails[0].split():
            typ, data = con.fetch(num, '(RFC822)')
            msgs.append(data)

    #
    #
    #
    def sendmail(self, email_html_template = None, data = None, reciever_email = []):
        email_html_template = get_template(email_html_template).render(data)
        email_msg = EmailMessage(msg_body, email_html_template, self.app_email, receiver_email, reply_to = self.reply_email)
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)



#******************************************************************************
# ADMIN EMAIL VIEW
#******************************************************************************

class AdminEmailView(View):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/staff/email_management.html'

    data["page_title"] = "Email Management"

    data["css_files"] = ['custom_files/css/email.css']
    data["js_files"] = []

    #
    #
    #

    def get(self, request):
        return render(request, self.template_name, self.data)

    #
    #
    #

    def post(self, request):
        pass

    #
    #
    #
