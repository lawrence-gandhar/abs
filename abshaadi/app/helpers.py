from dateutil.relativedelta import *
from datetime import date, datetime
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


import hashlib

#
# CALCULATE AGE FROM DOB
#

def get_age_from_dob(dob, only_years = False):
    today = date.today()
    dob = datetime.strptime(dob,"%Y-%m-%d")
    age = relativedelta(today, dob)

    if only_years:
        return age.years
    return age


#
# CALCULATE YEAR OF BIRTH FROM AGE
#

def get_birth_year_from_age(age):
    today = date.today()
    year_of_birth = datetime.now() - relativedelta(years=int(age))

    return year_of_birth.strftime("%Y")

#
# CALCULATE YEAR-01-01 OF BIRTH FROM AGE
#

def get_birth_full_from_age(age):

    today = date.today()
    year_of_birth = datetime.now() - relativedelta(years=int(age))

    yr = year_of_birth.strftime("%Y")

    return "{}-{}-{}".format(yr,"01","01")


#******************************************************************************
# Send Email
#******************************************************************************

def send_email_from_app(email, id, template):

    id = id+"<_secret_>"+settings.SECRET_KEY

    result = hashlib.sha384(id.encode())

    data =  {'email': email, 'uid':id, 'qstr':result.hexdigest()}

    email_html_template = get_template(template).render(data)
    receiver_email = email
    email_msg = EmailMessage('Welcome from ATUT BANDHAN SHAADI',
                                email_html_template,
                                settings. APPLICATION_EMAIL,
                                [receiver_email],
                                reply_to=[settings.APPLICATION_EMAIL]
                                )
    # this is the crucial part that sends email as html content but not as a plain text
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)
