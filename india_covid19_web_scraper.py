import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pytz
import pandas as pd

COVID19_INDIA_URL_OFFICIAL = "https://www.mohfw.gov.in/"

NOW_TIMESTAMP_ET = datetime.now(pytz.timezone("US/Eastern")).strftime('%Y-%m-%d-%H:%M:%S')
NOW_TIMESTAMP_IST = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d-%H:%M:%S')


def web_scraping_for_india_covid19():

    page = requests.get(COVID19_INDIA_URL_OFFICIAL)
    assert page.status_code == 200, 'Request to page did NOT respond with status code 200.'

    soup = BeautifulSoup(page.content, 'html.parser')

    national_data = soup.find('div', class_='site-stats-count').findChildren(name='li')

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

    print('\nCOVID-19 Data from India at {} IST ({} ET)'.format(NOW_TIMESTAMP_IST, NOW_TIMESTAMP_ET))
    print('\nNational Level Data:')
    print(national_output_dict)

    sub_national_data = soup.find('div', class_='data-table table-responsive').findChild(class_='table table-striped')

    sub_national_output_data = []

    table_headings = [heading.text.strip() for heading in sub_national_data.find('thead').find_all('th')]
    table_rows = sub_national_data.find('tbody').find_all('tr')

    for row in table_rows:
        state_row = [item.text.strip() for item in row.find_all('td')]
        sub_national_output_data.append(state_row)

    sub_national_output_data = sub_national_output_data[:len(sub_national_output_data)-2]

    sub_national_output_df = pd.DataFrame.from_records(sub_national_output_data)
    sub_national_output_df.columns = table_headings
    del sub_national_output_df['S. No.']

    for col in sub_national_output_df.columns[1:]:
        sub_national_output_df[col] = pd.to_numeric(sub_national_output_df[col])

    print('\nSub-national Level Data:')
    print(sub_national_output_df.to_markdown())

    return national_output_dict, sub_national_output_df


if __name__ == '__main__':
    web_scraping_for_india_covid19()
