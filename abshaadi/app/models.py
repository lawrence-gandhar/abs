from django.db import models

# Create your models here.

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
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
    )
    
    is_active = models.BooleanField(
        default = True,
        db_index = True,
    )

    def __str__(self):
        return self.religion_name.upper()

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
        return self.caste_name.upper()

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
        return self.country_name.upper()

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
        return self.state_name.upper()

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
        return self.city_name.upper()

    class Meta:
        verbose_name_plural = "Cities List"


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

      
 
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
    
    aged_from = models.IntegerField(
        db_index = True,
        null = True,
        blank = False,
    )
    
    aged_to = models.IntegerField(
        db_index = True,
        null = True,
        blank = False,
    )
    
    father_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )
    
    mother_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
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
    
    complexion = models.CharField(
        max_length = 50,
        db_index = True,
        null = True,
        blank = False,
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
    
    qualification = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )
    
    job_details = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
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
        blank = False,
    )
    
    address = models.TextField(
        db_index = True,
        null = True,
        blank = False,
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
        null = True,
        blank = True,
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
    
    def __str__(self):
        return self.fullname.upper()

    class Meta:
        verbose_name_plural = "User Profiles"
    
    
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
        null = True,
        default = False,
        blank = True,
    )
    
    class Meta:
        verbose_name_plural = "User Profile Pictures"
    
    
#***********************************************************************
#
#***********************************************************************
 
class Looking_For_Cities(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    city = models.ForeignKey(
        Countries_Cities,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    ) 
    
    class Meta:
        verbose_name_plural = "Cities Filter"

#***********************************************************************
#
#***********************************************************************

class Looking_For_States(models.Model):    
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    c_states = models.ForeignKey(
        Countries_States,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    ) 
    
    class Meta:
        verbose_name_plural = "State Filters"
    
#***********************************************************************
#
#***********************************************************************

class Looking_For_Countries(models.Model):    
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    country = models.ForeignKey(
        Countries,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    ) 

    class Meta:
        verbose_name_plural = "Countries Filters"    
    

#***********************************************************************
#
#***********************************************************************

class Looking_For_Religions(models.Model):  
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
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
    
    class Meta:
        verbose_name_plural = "Religion Filters"
 
#***********************************************************************
#
#***********************************************************************

class Looking_For_Attr(models.Model): 
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
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
    
    complexion = models.CharField(
        max_length = 50,
        db_index = True,
        null = True,
        blank = False,
    )
    
    class Meta:
        verbose_name_plural = "Attributes Filters"

#***********************************************************************
#
#***********************************************************************

class Looking_For_Jobs(models.Model): 
    user = models.ForeignKey(
        CustomUser,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
    )

    qualification = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )
    
    job_details = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = False,
    )
    
    class Meta:
        verbose_name_plural = "Job Filters"
    

#***********************************************************************
#
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
    
    seen_on = models.DateTimeField(
        db_index = True,
        null = True,
        blank = True,
    )
    
    class Meta:
        verbose_name_plural = "Message Center"
    

#***********************************************************************
#
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
#
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
        null = True,
    )
    
    class Meta:
        verbose_name_plural = "Paid Users"
        
    
#***********************************************************************
#
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
    
    
    
    
    
    
    