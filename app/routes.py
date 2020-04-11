from app import app
from bs4 import BeautifulSoup
import requests
from flask import render_template


url = requests.get('https://ncov2019.live/').text
soup = BeautifulSoup(url, 'html.parser')

@app.route('/')
def corona():
    country = [] 
    confirmed= []
    death = []

    total_confirmed_cases = soup.find_all("p")[3].text
    total_death = soup.find_all("p")[5].text
    #Parse data that are stored between <tr> ..</tr> of HTML 
    tables = soup.find('table', id='sortable_table_global')
    headings = tables.findAll('thead')
    head = [heading.text.strip() for heading in headings]
    if (head[:5] == ['Name', 'Confirmed', 'Changes', 'percentChange','Deceased']):
        pass
    for table_row in tables.findAll('tr')[2:20]: 
        table_data = table_row.find_all('td')
        if not table_data:
            continue    
        name , confirm , changes, percentChange, deceased = [tbd.text for tbd in table_data[:5]]
        country.append(name.strip())

        confirmed.append(confirm.strip())
        death.append(deceased)
        
    return render_template('index.html',total_confirmed_cases=total_confirmed_cases, total_death=total_death,country=country,death=death,confirmed=confirmed)
