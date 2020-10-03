import sqlite3, json

conn = sqlite3.connect('E:\\lawrence_works\\abs\\abshaadi\\db.sqlite3')
cur = conn.cursor()
"""
cur.execute('Delete from app_countries')
cur.execute('Delete from app_countries_states')
cur.execute('Delete from app_countries_cities')


cur.execute('UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM app_countries) WHERE name="app_countries"')
cur.execute('UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM app_countries_states) WHERE name="app_countries_states"')
cur.execute('UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM app_countries_cities) WHERE name="app_countries_cities"')

conn.commit()
"""

cur.execute('Delete from app_countries_cities')
cur.execute('UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM app_countries_cities) WHERE name="app_countries_cities"')
conn.commit()


COUNTRIES_LIST = "E:\\lawrence_works\\abs\\abshaadi\\app\static\\site_managers\\countries+states+cities.txt"


with open(COUNTRIES_LIST, 'r', encoding='utf-8') as file:
    data = json.load(file)
    
    """    
    for row in data:
        cur.execute('insert into app_countries (country_name, is_active) values("{}", 1)'.format(row["name"]))
        conn.commit()
    
    
    cur.execute('Delete from app_countries_states')
    cur.execute('UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM app_countries_states) WHERE name="app_countries_states"')
    conn.commit()
    
    """
    
    cur.execute('SELECT id, country_name FROM app_countries')
    countries = cur.fetchall()
    
    for country in countries:
        
        for d_row in data:
            if d_row["name"] == country[1]:
                for state in d_row["states"]:
                    
                    if "name" in state.keys():
                        #cur.execute('insert into app_countries_states (country_id, state_name, is_active) values("{}","{}", 1)'.format(country[0], state["name"], 1))
                        #conn.commit()   
                    
                        cur.execute('SELECT id, country_id, state_name FROM app_countries_states where state_name = "{}" and country_id = {} order by id desc limit 1'.format(state["name"], country[0]))
                        states = cur.fetchone()
                    
                        print(states)
                    
                        for city in state["cities"]:  
                            cur.execute('insert into app_countries_cities (country_id, state_name_id, city_name, is_active) values("{}","{}", "{}", 1)'.format(country[0], states[0], city["name"], 1))
                            conn.commit() 
                    
                    else:
                        for city in state["cities"]:  
                            cur.execute('insert into app_countries_cities (country_id, state_name_id, city_name, is_active) values("{}","{}", "{}", 1)'.format(country[0], None, city["name"], 1))
                            conn.commit() 
                    
                    