import email, imaplib
from django.conf import settings
from collections import defaultdict


#******************************************************************************
# EMAIL MANAGEMENT
#******************************************************************************

class EmailManagement():

    def __init__(self):
        self.username = settings.EMAIL_HOST_USER
        self.passwd = settings.EMAIL_HOST_PASSWORD
        self.imap_url = 'imap.gmail.com'
        self.conn = None

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
    def sent(self):
        pass
