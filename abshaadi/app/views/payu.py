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
from app.forms import registration_forms, search_forms

from app.helpers import *

import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
