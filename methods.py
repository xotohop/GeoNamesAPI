import pandas as pd
import json
import re

from helpers import cities_cleaner, north, tz_diff

try:
    data = pd.read_table('RU.txt', delimiter='\t', names=['geonameid', 'name', 'asciiname', 'alternatenames',
                                                        'latitude', 'longitude',
                                                        'feature class', 'feature code', 'country code', 'cc2',
                                                        'admin1 code', 'admin2 code', 'admin3 code', 'admin4 code',
                                                        'population', 'elevation', 'dem',
                                                        'timezone', 'modification date'],
                                                        low_memory=False)
    data.fillna('', inplace=True)
except FileNotFoundError:
    print('File RU.txt not found')
    exit()


def get_city_by_geonameid(geonameid):
    ''' Returns information about a city by its geonameid '''
    
    try:
        city = data[(data['geonameid'] == int(geonameid)) & (data['feature class'] == 'P')]
    except ValueError:
        return {}
    
    city['alternatenames'] = city['alternatenames'].apply(lambda x: x.split(','))

    return json.dumps(city.to_dict(orient='records'), indent=4, ensure_ascii=False)


def get_cities_list():
    '''  '''
    
    pass


def get_cities_by_name(city_name1, city_name2):
    '''
    Returns information about two cities by their name (in Russian), and also additionally: 
    which of them is located to the north and whether they have the same time zone
    '''
    
    try:
        city_name1 = str(city_name1)
        city_name2 = str(city_name2)
    except ValueError:
        return {}
    
    cities1 = data[(data['alternatenames'].str.contains(city_name1, na=False, case=False)) \
        & (data['feature class'] == 'P')].sort_values(by=['population'], ascending=False)
    cities2 = data[(data['alternatenames'].str.contains(city_name2, na=False, case=False)) \
        & (data['feature class'] == 'P')].sort_values(by=['population'], ascending=False)
    
    if len(cities1) == 0 or len(cities2) == 0:
        return {}
    
    city1 = cities_cleaner(city_name1, cities1)
    city2 = cities_cleaner(city_name2, cities2)
    
    if len(city1) == 0 or len(city2) == 0:
        return {}
    else:
        city1 = city1.iloc[0]
        city2 = city2.iloc[0]

    lst = []
    lst.append(city1.to_dict())
    lst.append(city2.to_dict())
    lst.append(north(city1, city2))
    lst.append(tz_diff(city1, city2))
    
    return json.dumps(lst, indent=4, ensure_ascii=False)


def get_cities_names(city_name):
    ''' Returns a hint with possible continuation options for city name '''
    
    city_name = str(city_name)
    cities = data[(data['alternatenames'].str.contains(city_name, na=False, case=False)) \
        & (data['feature class'] == 'P')].sort_values(by=['population'], ascending=False)
    cities['alternatenames'] = cities['alternatenames'].apply(lambda x: x.split(','))
    
    lst = []
    for city in cities['alternatenames']:
        for alternatename in city:
            if city_name.lower() in alternatename.lower() and alternatename not in lst\
                and re.search('[а-яА-ЯёЁ]', alternatename):
                lst.append(alternatename)

    return json.dumps(lst, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # 2013159 - Yakutsk
    print(get_city_by_geonameid('2013159'))
    # print()
    # print(get_cities_by_name('Санкт-Петербург', 'Якутск'))
    # print(get_cities_names('66'))
