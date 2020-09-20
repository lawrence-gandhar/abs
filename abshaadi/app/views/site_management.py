import urllib.request
import json
from django.conf import settings
import os
from django.http import HttpResponse
from app.models import *
from django.utils import safestring 


#******************************************************************************
# LOAD COUNTRIES INTO DB
#******************************************************************************   

COUNTRIES_LIST = os.path.join(settings.STATICFILES_DIRS[0], 'site_managers')
COUNTRIES_LIST = os.path.join(COUNTRIES_LIST,'countries+states+cities.txt')


def add_countries_to_db(request):

    with open(COUNTRIES_LIST, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        Countries.objects.all().delete()
        Countries_States.objects.all().delete()
        Countries_Cities.objects.all().delete()
        
        for row in data:
            country = Countries(
                country_name = row["name"]
            )
            
            country.save()
            
            
            for state in row["states"]:
                if "name" in state.keys():            
                    if state["name"]:
                    
                        state_ins = Countries_States(
                            country = country,
                            state_name = state["name"]
                        )
                        
                        state_ins.save()
                        
                    for city in state["cities"]:
                    
                        city_ins = Countries_Cities(
                            country = country,
                            state_name = state_ins,
                            city_name = city["name"]
                        )
                    
                        city_ins.save()
                
                else:
                    for city in state["cities"]:
                    
                        city_ins = Countries_Cities(
                            country = country,
                            state_name = state_ins,
                            city_name = city["name"]
                        )
                    
                        city_ins.save()
                   
    return HttpResponse('1')
    

#******************************************************************************
# FETCH STATES HTML DROPDOWN
#****************************************************************************** 

def get_states_dropdown(request, id):
    
    if id is not None:
    
        html = []
    
        try:
            country = Countries.objects.get(pk = id)
        except:
            return HttpResponse('')
          
        states = Countries_States.objects.filter(country = country)

        if states is not None:
            for state in states:
                html.append("<option value='{}'>{}</option>".format(state.id, state))
            return HttpResponse(safestring.mark_safe(''.join(html)))
        else:
            return HttpResponse('')
