import requests
from bs4 import BeautifulSoup, element
from datetime import datetime

COVID19_INDIA_URL_OFFICIAL = "https://www.mohfw.gov.in/"
DATE_TODAY = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

page = requests.get(COVID19_INDIA_URL_OFFICIAL)
assert page.status_code == 200, 'Request to page did NOT respond with status code 200.'

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

soup_children_list = list(soup.children)

site_stats_index = None
state_data_index = None

for item in soup_children_list:
    if '<div class="site-stats-count">' in str(item):
        site_stats_index = soup_children_list.index(item)
    if '<section class="site-update" id="state-data">' in str(item):
        state_data_index = soup_children_list.index(item)

site_stats_html = soup_children_list[site_stats_index]
state_data_html = soup_children_list[state_data_index]

if not isinstance(site_stats_html, element.Tag):
    raise TypeError('Wrong BeautifulSoup object type. Need <bs4.element.Tag>')

if not isinstance(state_data_html, element.Tag):
    raise TypeError('Wrong BeautifulSoup object type. Need <bs4.element.Tag>')

# soup_children_type_list = [type(item) for item in soup_children_list]

children = list(list(list(site_stats_html.children)[1].children)[1].children)
# print(children)



print(soup.find_all('div', class_='site-stats-count'))
# print(soup.find_all('div', class_='data-table table-responsive'))

