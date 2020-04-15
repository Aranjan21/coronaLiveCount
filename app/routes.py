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
    total_recovered = soup.find_all("p")[9].text
    #Parse data that are stored between <tr> ..</tr> of HTML 
    tables = soup.find('table', id='sortable_table_global')
    headings = tables.findAll('thead')
    head = [heading.text.strip() for heading in headings]
    if (head[:5] == ['Name', 'Confirmed', 'Changes', 'percentChange','Deceased']):
        pass
    for table_row in tables.findAll('tr')[2:30]: 
        table_data = table_row.find_all('td')
        if not table_data:
            continue    
        name , confirm , changes, percentChange, deceased = [tbd.text for tbd in table_data[:5]]
        country.append(name.strip())

        confirmed.append(confirm.strip())
        death.append(deceased)
        
    return render_template('index.html',total_confirmed_cases=total_confirmed_cases, total_death=total_death,total_recovered=total_recovered,country=country,death=death,confirmed=confirmed)

@app.route('/wiki')
def wiki():
    """
    Render the corona facts  template on the /CoronaFacts route
    """
    return render_template('corona_facts.html')

@app.route('/india')
def india():
    """
    Render the INDIA template on the /CoronaFacts route
    """
    state = []
    confirmed = []
    death = []
    url2 = requests.get('https://www.mohfw.gov.in/').text
    soup = BeautifulSoup(url2, 'html.parser')

    total_confirmed_cases = soup.find_all("strong")[6].text
    total_death = soup.find_all("strong")[8].text
    total_recovered = soup.find_all("strong")[7].text

    #Parse data that are stored between <tr>...</tr>  

    table = soup.find('table', {'class':'table table-striped'})
    thead = table.findAll('thead')
    head = [heading.text.strip() for heading in thead]

    
    if (head[1:4] == ['S. No., Name of State / UT, Total Confirmed cases (Including 76 foreign Nationals) ,Cured/Discharged/Migrated, Death']):
        pass  
    for table_row in table.findAll('tr'):
        table_data = (table_row.find_all('td'))
        if not table_data:
            continue
        
        name = [tbd.text for tbd in table_data[1:2]]
        confirm = [tbd.text for tbd in table_data[2:3]]
        dead = [tbd.text for tbd in table_data[4:5]]
        state.append(' '.join(name))
        confirmed.append(' '.join(confirm))
        death.append(' '.join(dead))
        
            
    return render_template('india.html',total_confirmed_cases=total_confirmed_cases,total_death=total_death,total_recovered=total_recovered,confirmed=confirmed,state=state,death=death,table_data=table_data)

