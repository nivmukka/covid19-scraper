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

    '''
    National Level Data
    '''

    # national data is in a `div` with an unordered list as a child
    national_data = soup.find('div', class_='site-stats-count').findChildren(name='li')

    # dictionary to collect national level case counts
    national_output_dict = {}

    # the list has items, each item corresponds to case counts for active, recovered, deaths, migrated
    # looping through the list and stripping out the text to get case counts for each category
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

    # adding up all case count categories to get total number of cases
    national_output_dict['Cases'] = sum(list(national_output_dict.values()))

    print('\nCOVID-19 Data from India at {} IST ({} ET)'.format(NOW_TIMESTAMP_IST, NOW_TIMESTAMP_ET))
    print('\nNational Level Data:')
    print(national_output_dict)

    '''
    Sub-National Level Data
    '''

    # sub-national data is in a table, which is a child of a div
    sub_national_data = soup.find('div', class_='data-table table-responsive').findChild(class_='table table-striped')

    # list to collect case counts of states at sub-national level
    # this is a list of lists
    sub_national_output_data = []

    # getting table headings from all `th`s in the `thead`
    table_headings = [heading.text.strip() for heading in sub_national_data.find('thead').find_all('th')]

    # getting table rows from all `tr`s in the `tbody`
    # each row corresponds to a state
    table_rows = sub_national_data.find('tbody').find_all('tr')

    # getting text from each cell of the table by using `td`s
    # putting the row of `td`s in a list
    # appending list to `sub_national_output_data` (list of lists)
    for row in table_rows:
        state_row = [item.text.strip() for item in row.find_all('td')]
        sub_national_output_data.append(state_row)

    # deleting the last two rows from the table because they have unrelated text
    sub_national_output_data = sub_national_output_data[:len(sub_national_output_data)-2]

    # putting the list of lists into a pandas data frame
    sub_national_output_df = pd.DataFrame.from_records(sub_national_output_data)

    # assigning table headings to data frame columns
    sub_national_output_df.columns = table_headings

    # deleting the `S. No.` column
    del sub_national_output_df['S. No.']

    # converting the last three columns to numeric data types
    for col in sub_national_output_df.columns[1:]:
        sub_national_output_df[col] = pd.to_numeric(sub_national_output_df[col])

    print('\nSub-national Level Data:')
    print(sub_national_output_df.to_markdown())

    return national_output_dict, sub_national_output_df


if __name__ == '__main__':
    web_scraping_for_india_covid19()
