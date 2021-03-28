from django.db import models

# Create your models here.

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings

import uuid
import os


#***********************************************************************
#
#***********************************************************************

class Religion(models.Model):
    religion_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
        unique = True,
    )

    is_active = models.BooleanField(
        default = True,
        db_index = True,
    )

    def __str__(self):
        return self.religion_name.title()

    class Meta:
        verbose_name_plural = "Religions"


#***********************************************************************
#
#***********************************************************************

class Caste(models.Model):
    religion = models.ForeignKey(
        Religion,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    caste_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    is_active = models.BooleanField(
        default = True,
        db_index = True,
    )

    def __str__(self):
        return self.caste_name.title()

    class Meta:
        verbose_name_plural = "Religious Castes"

#***********************************************************************
#
#***********************************************************************

class Countries(models.Model):
    country_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    is_active = models.BooleanField(
        default = True,
        db_index = True,
    )

    def __str__(self):
        return self.country_name.title()

    class Meta:
        verbose_name_plural = "Countries List"

#***********************************************************************
#
#***********************************************************************

class Countries_States(models.Model):
    country = models.ForeignKey(
        Countries,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    state_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    is_active = models.BooleanField(
        default = True,
        db_index = True,
    )

    def __str__(self):
        return self.state_name.title()

    class Meta:
        verbose_name_plural = "States List"

#***********************************************************************
#
#***********************************************************************

class Countries_Cities(models.Model):
    country = models.ForeignKey(
        Countries,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    state_name = models.ForeignKey(
        Countries_States,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    city_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    is_active = models.BooleanField(
        default = True,
        db_index = True,
    )

    def __str__(self):
        return self.city_name.title()

    class Meta:
        verbose_name_plural = "Cities List"



#***********************************************************************
#
#***********************************************************************

class Qualifications(models.Model):

    IS_TRUE = ((True, 'YES'), (False, 'NO'))

    qualification = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    is_active = models.BooleanField(
        default = True,
        choices = IS_TRUE,
        db_index = True,
    )

    def __str__(self):
        return self.qualification.title()

    class Meta:
        verbose_name_plural = "Qualifications Filters"

#***********************************************************************
#
#***********************************************************************

class Job_Types(models.Model):

    IS_TRUE = ((True, 'YES'), (False, 'NO'))

    job_type = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    is_active = models.BooleanField(
        default = True,
        choices = IS_TRUE,
        db_index = True,
    )

    def __str__(self):
        return self.job_type.title()

    class Meta:
        verbose_name_plural = "Job Types Filters"

#***********************************************************************
# JOBS MODEL
#***********************************************************************

class Jobs(models.Model):

    IS_TRUE = ((True, 'YES'), (False, 'NO'))

    job_details = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    is_active = models.BooleanField(
        default = True,
        choices = IS_TRUE,
        db_index = True,
    )

    def __str__(self):
        return self.job_details.capitalize()

    class Meta:
        verbose_name_plural = "Jobs Filters"


#***********************************************************************
# COMPLEXIONS MODEL
#***********************************************************************

class Complexions(models.Model):

    IS_TRUE = ((True, 'YES'), (False, 'NO'))

    complexion_details = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    is_active = models.BooleanField(
        default = True,
        choices = IS_TRUE,
        db_index = True,
    )

    def __str__(self):
        return self.complexion_details.capitalize()

    class Meta:
        verbose_name_plural = "Complexion Filters"


#***********************************************************************
#
#***********************************************************************

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


#***********************************************************************
#
#***********************************************************************

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    email_verified = models.BooleanField(
        default = False,
        db_index = True,
    )

    subscribe_email = models.BooleanField(
        default = False,
        db_index = True,
    )

    subscribe_sms = models.BooleanField(
        default = False,
        db_index = True,
    )

    subscribe_whatsapp = models.BooleanField(
        default = False,
        db_index = True,
    )

    online_now = models.BooleanField(
        db_index = True,
        default = False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_delete, sender=CustomUser)
def delete_file(sender, instance, *args, **kwargs):

    path = os.path.join(settings.MEDIA_ROOT, str(instance.id))
    try:
        os.rmdir(path)
    except:
        pass




#***********************************************************************
# PACKAGES
#***********************************************************************

class Package(models.Model):

    TENURE_TYPE = (
        (1, "Years"),
        (2, "Months"),
        (3, "Weeks"),
    )

    IS_TRUE = ((True, 'YES'), (False, 'NO'))

    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    package_name = models.CharField(
        max_length = 255,
        blank = False,
        null = False,
        unique = True,
    )

    value = models.IntegerField(
        db_index = True,
        null = False,
        blank = False,
    )

    tenure = models.IntegerField(
        db_index = True,
        null = False,
        blank = False,
    )

    tenure_types = models.IntegerField(
        default = 1,
        choices = TENURE_TYPE,
        db_index = True,
    )

    description = models.TextField(
        null = True,
        blank = True,
    )

    is_active = models.BooleanField(
        default = True,
        choices = IS_TRUE,
        db_index = True,
    )

    created_on = models.DateTimeField(
        auto_now_add = True,
        db_index = True,
        null = True,
        blank = True,
    )

    class Meta:
        verbose_name_plural = "Packages"

    def __str__(self):
        return self.package_name.capitalize()


#***********************************************************************
# PROFILE
#***********************************************************************

class ConfirmEmail(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    key = models.CharField(
        max_length = 50,
        db_index = True,
        null = True,
        blank = True
    )

    class Meta:
        verbose_name_plural = "Confirm Emails"

#***********************************************************************
# PROFILE
#***********************************************************************

class Profile(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    uid = models.CharField(
        max_length = 20,
        blank = True,
        null = True,
        db_index = True,
    )

    package = models.ForeignKey(
        Package,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    fullname = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )

    MALE = 'M'
    FEMALE = 'F'

    gender_choices = ((MALE, 'Male'), (FEMALE, 'Female'))

    gender = models.CharField(
        max_length = 1,
        db_index = True,
        null = True,
        blank = False,
        choices = gender_choices,
    )

    looking_for_gender = models.CharField(
        max_length = 1,
        db_index = True,
        null = True,
        blank = False,
        choices = gender_choices,
    )


    FAMILY_TYPE = (
        (1, "Nuclear"),
        (2, "Single Parent Family"),
        (3, "Joint Family"),
        (4, "Grandparent Family"),
        (5, "Step Family"),
    )

    family_type = models.IntegerField(
        blank = True,
        null = True,
        db_index = True,
        choices = FAMILY_TYPE
    )

    FAMILY_VALUES = (
        (1, "Traditional"),
        (2, "Liberal"),
        (3, "Orthodox"),
        (4, "Religious"),
    )

    family_values = models.IntegerField(
        blank = True,
        null = True,
        db_index = True,
        choices = FAMILY_VALUES
    )

    father_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = True,
    )

    mother_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = True,
    )

    father_job = models.ForeignKey(
        Jobs,
        related_name = 'father_job',
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    mother_job = models.ForeignKey(
        Jobs,
        related_name = 'mother_job',
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    siblings = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    sibling_male = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    sibling_female = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    sibling_elder = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    sibling_younger = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    sibling_married = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    dob = models.DateField(
        db_index = True,
        null = True,
        blank = False,
    )

    height = models.IntegerField(
        db_index = True,
        null = True,
        blank = False,
    )

    weight = models.IntegerField(
        db_index = True,
        null = True,
        blank = False,
    )

    complexion = models.ForeignKey(
        Complexions,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    religion = models.ForeignKey(
        Religion,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    caste_creed = models.ForeignKey(
        Caste,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    qualification = models.ForeignKey(
        Qualifications,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )


    job_type = models.ForeignKey(
        Job_Types,
        db_index = True,
        blank = True,
        null = True,
        on_delete = models.SET_NULL,
    )

    job_details = models.ForeignKey(
        Jobs,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    phone_number = models.CharField(
        max_length = 20,
        db_index = True,
        null = True,
        blank = False,
    )

    phone_number_alternative = models.CharField(
        max_length = 20,
        db_index = True,
        null = True,
        blank = True,
    )

    phone_number_verified = models.BooleanField(
        default = False,
        db_index = True,
    )

    address = models.TextField(
        null = True,
        blank = False,
    )

    country = models.ForeignKey(
        Countries,
        db_index = True,
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name = 'my_country',
    )

    state = models.ForeignKey(
        Countries_States,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = 'my_state',
    )

    city = models.ForeignKey(
        Countries_Cities,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = 'my_city',
    )


    biodata = models.FileField(
        upload_to = 'resumes',
        null = True,
        blank = True,
    )

    descriptions = models.TextField(
        null = True,
        blank = True,
    )

    block_profile_pics = models.BooleanField(
        default = False,
        db_index = True,
        blank = True,
    )

    partner_preference = models.TextField(
        blank = True,
        null = True,
    )

    created_on = models.DateTimeField(
        auto_now_add = True,
        db_index = True,
        null = True,
        blank = True,
    )

    updated_on = models.DateTimeField(
        auto_now_add = False,
        db_index = True,
        null = True,
        blank = True,
    )

    assigned_to = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "assigned_to_staff"
    )


    class Meta:
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=Profile)
def create_uuid(sender, instance, created, **kwargs):
    if created:
        instance.uid = 'AB-{}'.format(1000000 + instance.user.id)
        instance.save()

#***********************************************************************
#
#***********************************************************************

def profile_pics_directory(instance, filename):
    f_path = os.path.join(str(instance.user.id), str(uuid.uuid4())+".jpg")
    print(f_path)
    return f_path


class ProfilePictures(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    picture = models.FileField(
        upload_to = profile_pics_directory,
        null = True,
        blank = True,
    )

    set_as_profile_pic = models.BooleanField(
        db_index = True,
        default = False,
        blank = True,
    )

    class Meta:
        verbose_name_plural = "User Profile Pictures"


#***********************************************************************
# FILTERS MODEL
#***********************************************************************

class MyFilters(models.Model):

    IS_TRUE = ((True, 'YES'), (False, 'NO'))

    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    filter_name = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    l_attr = models.TextField(
        null = True,
        blank = True,
    )

    l_cities = models.ManyToManyField(
        Countries_Cities,
        blank = True,
        db_index = True,
    )

    l_states = models.ManyToManyField(
        Countries_States,
        blank = True,
        db_index = True,
    )

    l_countries = models.ManyToManyField(
        Countries,
        blank = True,
        db_index = True,
    )

    l_religions = models.ManyToManyField(
        Religion,
        blank = True,
        db_index = True,
    )

    l_caste = models.ManyToManyField(
        Caste,
        blank = True,
        db_index = True,
    )

    l_qualifications = models.ManyToManyField(
        Qualifications,
        db_index = True,
        blank = True,
    )

    job_type = models.ManyToManyField(
        Job_Types,
        db_index = True,
        blank = True,
    )

    l_jobs = models.ManyToManyField(
        Jobs,
        db_index = True,
        blank = True,
    )

    l_complexions = models.ManyToManyField(
        Complexions,
        db_index = True,
        blank = True,
    )

    aged_from = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    aged_to = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    is_active = models.BooleanField(
        default = True,
        choices = IS_TRUE,
        db_index = True,
    )

    class Meta:
        verbose_name_plural = "Filters Table"


#***********************************************************************
# PARTNER PREFERENCES MODEL
#***********************************************************************

class Partner_Preferences(models.Model):

    IS_TRUE = ((True, 'YES'), (False, 'NO'))

    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    l_attr = models.TextField(
        null = True,
        blank = True,
    )

    l_cities = models.ManyToManyField(
        Countries_Cities,
        blank = True,
        db_index = True,
    )

    l_states = models.ManyToManyField(
        Countries_States,
        blank = True,
        db_index = True,
    )

    l_countries = models.ManyToManyField(
        Countries,
        blank = True,
        db_index = True,
    )

    l_religions = models.ManyToManyField(
        Religion,
        blank = True,
        db_index = True,
    )

    l_caste = models.ManyToManyField(
        Caste,
        blank = True,
        db_index = True,
    )

    l_qualifications = models.ManyToManyField(
        Qualifications,
        db_index = True,
        blank = True,
    )

    job_type = models.ManyToManyField(
        Job_Types,
        db_index = True,
        blank = True,
    )

    l_jobs = models.ManyToManyField(
        Jobs,
        db_index = True,
        blank = True,
    )

    l_complexions = models.ManyToManyField(
        Complexions,
        db_index = True,
        blank = True,
    )

    aged_from = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    aged_to = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    class Meta:
        verbose_name_plural = "Partner Preferences Table"

#***********************************************************************
# MESSAGE CENTER MODEL
#***********************************************************************

class MessageCenter(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    to_user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
        related_name = 'to_user'
    )

    created_on = models.DateTimeField(
        auto_now_add = True,
        db_index = True,
        null = True,
        blank = True,
    )

    class Meta:
        verbose_name_plural = "Message Thread Center"


class MessageHistory(models.Model):

    msg = models.ForeignKey(
        MessageCenter,
        on_delete = models.CASCADE,
        db_index = True,
    )

    message = models.TextField(
        null = False,
        blank = False,
    )

    seen = models.BooleanField(
        db_index = True,
        default = False,
    )

    sent_on = models.DateTimeField(
        db_index = True,
        auto_now_add = True,
    )

    class Meta:
        verbose_name_plural = "Message History"




#***********************************************************************
# REPORT USER
#***********************************************************************

class ReportUser(models.Model):

    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    to_user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
        related_name = 'report_user'
    )

    report_description = models.TextField(
        blank = False,
        null = True,
    )

    created_on = models.DateTimeField(
        auto_now_add = True,
        db_index = True,
        null = True,
        blank = True,
    )

    class Meta:
        verbose_name_plural = "Report User Center"



#***********************************************************************
# PAID USER
#***********************************************************************

class PaidUser(models.Model):

    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    package = models.ForeignKey(
        Package,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    is_active = models.BooleanField(
        default = True,
        db_index = True,
    )

    class Meta:
        verbose_name_plural = "Paid Users"


#***********************************************************************
# PAYMENT DETAILS
#***********************************************************************

class PaymentDetails(models.Model):

    payment_choices = (
        (1, "Credit Card"),
        (2, "Debit Card"),
        (3, "Online Transfer"),
        (4, "Cash"),
        (5, "Cheque"),
    )

    user = models.ForeignKey(
        PaidUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    payment_type = models.IntegerField(
        choices = payment_choices,
        db_index = True,
        blank = True,
        null = True,
    )

    paid_on = models.DateTimeField(
        auto_now_add = False,
        db_index = True,
        null = True,
        blank = True,
    )

    package = models.ForeignKey(
        Package,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    class Meta:
        verbose_name_plural = "Payment Details"


#***********************************************************************
# PROFILE LIKE
#***********************************************************************

class ProfileLike(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    by_user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
        related_name = 'by_user'
    )

    viewed = models.BooleanField(
        default = False,
        db_index = True,
    )

    shortlisted = models.BooleanField(
        default = False,
        db_index = True,
    )

    liked = models.BooleanField(
        default = False,
        db_index = True,
    )

    viewed_on = models.DateTimeField(
        db_index = True,
        null = True,
    )

    shortlisted_on = models.DateTimeField(
        db_index = True,
        null = True,
    )

    liked_on =  models.DateTimeField(
        db_index = True,
        null = True,
    )

    class Meta:
        verbose_name_plural = "Profile Like & Save"


#***********************************************************************
# Contact Us
#***********************************************************************

class ContactUs(models.Model):

    fullname = models.CharField(
        max_length = 250,
        null = False,
        blank = False,
    )

    email = models.EmailField(
        db_index = True,
        blank = False,
        null = False,
    )

    phone = models.CharField(
        db_index = True,
        blank = False,
        null = False,
        max_length = 20,
    )

    message = models.TextField(
        blank = False,
        null = False,
    )

    created_on = models.DateTimeField(
        auto_now_add = True,
        db_index = True,
    )

    class Meta:
        verbose_name_plural = "Contact Us"


#***********************************************************************
# Payment Gateway Settings
#***********************************************************************

class PaymentGatewayDetails(models.Model):

    name = models.CharField(
        max_length = 200,
        blank = False,
        null = False,
    )

    is_active = models.BooleanField(
        default = True,
        db_index = True,
    )

    api_link = models.TextField(
        blank = True,
        null = True,
    )

    merchant_id = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    api_key = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    api_secret = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    redirect_url = models.TextField(
        blank = True,
        null = True,
    )

    method_identifier = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.name.title()
