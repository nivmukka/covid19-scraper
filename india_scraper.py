import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

COVID19_INDIA_URL_OFFICIAL = "https://www.mohfw.gov.in/"
DATE_TODAY = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

page = requests.get(COVID19_INDIA_URL_OFFICIAL)
assert page.status_code == 200, 'Request to page did NOT respond with status code 200.'

soup = BeautifulSoup(page.content, 'html.parser')

national_data = soup.find('div', class_='site-stats-count').findChildren(name='li')
sub_national_data = soup.find('div', class_='data-table table-responsive')

national_output_dict = {}

for item in national_data:
    item = item.text.strip()

    if 'Active Cases' in item:
        national_output_dict['Active Cases'] = int(re.findall('[0-9]+', item)[0])

    if 'Cured / Discharged' in item:
        national_output_dict['Recovered Cases'] = int(re.findall('[0-9]+', item)[0])

    if 'Death' in item:
        national_output_dict['Deaths'] = int(re.findall('[0-9]+', item)[0])

    if 'Migrated' in item:
        national_output_dict['Migrated'] = int(re.findall('[0-9]+', item)[0])

national_output_dict['Cases'] = sum(list(national_output_dict.values()))

print(national_output_dict)
