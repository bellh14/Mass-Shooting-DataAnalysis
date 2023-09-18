from bs4 import BeautifulSoup
import requests
import lxml
import csv
import pandas as pd
import re
import json


# .loc[] gets row
# data[] gets col
# data.loc[][] gets specific index
data = pd.DataFrame(pd.read_csv('2014-2017_training_data.csv', delimiter=','))
extra_data = pd.DataFrame(pd.read_csv('extra_state_data.csv', delimiter=','))
training = pd.DataFrame(pd.read_csv("training.csv", delimiter=','))
land_mass = pd.DataFrame(pd.read_csv("Land_Mass.csv", delimiter=','))
dates = pd.DataFrame(pd.read_csv("Cities.csv", delimiter='\t'))
test_data = pd.DataFrame(pd.read_csv("2018_test_data.csv", delimiter=','))


def convert_dates():
    keys = ["Year", "Month", "Day"]
    for i in range(test_data.shape[0]):
        for key in keys:
            if key == "Year":
                test_data.loc[i, key] = ((test_data.loc[i, key] - 2014) + 1) / 4
            elif key == "Month":
                test_data.loc[i, key] = ((test_data.loc[i, key] - 1) + 1) / 12
            elif key == "Day":
                test_data.loc[i, key] = ((test_data.loc[i, key] - 1) + 1) / 31
    test_data.to_csv("2018_test_data.csv")


def transfer_land_mass_data():
    for i in range(test_data.shape[0]):
        for j in range(land_mass.shape[0]):
            if test_data.loc[i, "State"] == land_mass.loc[j, "State"]:
                test_data.loc[i, "Land Mass"] = land_mass.loc[j, "Land Mass"]
                break
    test_data.to_csv("2018_test_data.csv")


def parse_json_state_data():
    with open("state_data.json", 'r') as f:
        state_data = json.load(f)
    i = 0
    for state in state_data['data']:
        keys = ["State", "Population", "Year", "Household Income by Race", "Poverty Rate", "Property Value", "Median Age"]
        for key in keys:
            extra_data.loc[i, key] = state[key]
        i += 1
    extra_data.to_csv("extra_state_data.csv")


def transfer_state_data():
    keys = ["Population", "Year", "Household Income by Race", "Poverty Rate", "Property Value", "Median Age"]
    for i in range(test_data.shape[0]):
        for j in range(extra_data.shape[0]):
            t_date = test_data.loc[i, "Date"]
            ed_date = extra_data.loc[j, "Year"]
            ed_date = str(ed_date)
            if t_date[-1] == ed_date[-1]:
                if test_data.loc[i, "State"] == extra_data.loc[j, "State"]:
                    for key in keys:
                        test_data.loc[i, key] = extra_data.loc[j, key]
                    break

    test_data.to_csv("2018_test_data.csv")


def get_url(row):
    url = "https://www.city-data.com/crime/crime-"
    city = data.loc[row]["city_or_county"]  # may break
    city_name = city.split(' ')
    state = data.loc[row]["state"]
    state_name = state.split(' ')
    #url += city + "-" + state + ".html"
    for c in city_name:
        url += c + '-'
    for s in state_name:
        url += s + '-'

    if url[-1] == '-':
        url = url.rstrip(url[-1])
    url += ".html"
    return url


def get_violent_crime_rates(soup):
    raw_rates = []
    rates = []
    try:
        raw_rates = soup.find(id="violent-crime")
        raw_rates = raw_rates.text.split('\n')
        for rate in raw_rates:
            rate = rate.strip("Violent crime rate in ")
            rates.append(rate.split('U.S. '))
        rates = rates[2:6]

    except None:
        rates = 'failed'
    return rates


def get_property_crime_rates(soup):
    raw_rates = []
    rates = []
    try:
        raw_rates = soup.find(id="property-crime")
        raw_rates = raw_rates.text.split('\n')
        for rate in raw_rates:
            rate = rate.strip("Property crime rate in ")
            rates.append(rate.split('U.S. '))
    except None:
        rates = 'failed'
    return rates


def get_page(url):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=10)
    session.mount('https://', adapter)
    response = session.get(url)
    if not response.ok:
        print('Server responded:', response.status_code)
        return 404
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    try:
        events = soup.find_all(class_="event")
    except None:
        events = 'failed'
    return events


def get_data():
    url = "https://www.city-data.com/crime/crime-Muskegon-Michigan.html"
    rates = get_violent_crime_rates(get_page(url))
    p_rates = get_property_crime_rates(get_page(url))
    return rates


def process_crime_rates():

    for i in range(data.shape[0]):
        soup = get_page(get_url(i))
        if soup == 404:
            continue
        else:
            vcr = get_violent_crime_rates(soup)
        date = data.loc[i, "date"]
        for year in vcr:
            try:
                if year[0][3] == date[-1]:
                    data.loc[i, "Violent Crime Rate"] = year[0][-5:]
                    data.loc[i, "National VCR"] = year[1][-5:]
                    break
            except IndexError:
                print(year[0], date)


#process_crime_rates()

#data.to_csv('training_data.csv')
#parse_json_state_data()
#transfer_land_mass_data()
#transfer_state_data()
#convert_dates()