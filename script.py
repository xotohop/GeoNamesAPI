import pandas as pd
import re
from datetime import datetime
from pytz import timezone
from flask import Flask, request, jsonify

app = Flask(__name__)     
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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


def cities_cleaner(city_name, cities):
    ''' Returns DataFrame with alternatenames containing city_name '''
    
    cities['alternatenames'] = cities['alternatenames'].apply(lambda x: x.split(','))
    cities_clean = pd.DataFrame()
    for i in range(len(cities)):
        if city_name in cities.iloc[i]['alternatenames']:
            cities_clean = cities_clean.append(cities.iloc[i])
    
    return cities_clean


def north(city1, city2):
    ''' Returns the north of the two cities '''
    
    lat1 = city1['latitude']
    lat2 = city2['latitude']
    if lat1 > lat2:
        return {'north': f"{city1['name']} farther north of {city2['name']}"}
    elif lat1 == lat2:
        return {'north': f"{city1['name']} and {city2['name']} at the same latitude"}
    else:
        return {'north': f"{city2['name']} farther north of {city1['name']}"}


def tz_diff(city1, city2):
    ''' Returns the difference between timezones of two cities '''
    
    tz1 = timezone(city1['timezone'])
    tz2 = timezone(city2['timezone'])
    date = pd.to_datetime(datetime.now(tz=None))
    diff = (tz1.localize(date) - tz2.localize(date).astimezone(tz1)).seconds/3600
    if diff > 12.0:
        diff -= 24.0
    if abs(diff) == 0:
        return {'timezones_difference': 'Timezones are the same'}
    else:
        return {'timezones_difference': f"{abs(diff)} hour(s)"}


@app.route('/')
@app.route('/index')
def index():
    
    return '''
<html>
    <head>
        <title>InfoTeCS GeoNamesAPI</title>
    </head>
    <body>
        <h3>Доступные методы:</h3>
        <h3>get_city_by_geonameid</h3>
        <p>http://127.0.0.1:8000/get_city_by_geonameid?geonameid=<b>2013159</b></p>
        <h3>get_cities_list</h3>
        <p>http://127.0.0.1:8000/get_cities_list?page=<b>22</b>&size=<b>8</b></p>
        <p>http://127.0.0.1:8000/get_cities_list?size=<b>1337</b></p>
        <h3>get_cities_by_name</h3>
        <p>http://127.0.0.1:8000/get_cities_by_name?city_name1=<b>Москва</b>&city_name2=<b>Санкт-Петербург</b></p>
        <h3>get_cities_names</h3>
        <p>http://127.0.0.1:8000/get_cities_names?city_name=<b>москв</b></p>
    </body>
</html>'''


@app.route('/get_city_by_geonameid') 
def get_city_by_geonameid():
    ''' Returns information about a city by its geonameid '''
    
    geonameid = request.args.get('geonameid', type=int)
    
    city = data[(data['geonameid'] == geonameid) & (data['feature class'] == 'P')]
    city['alternatenames'] = city['alternatenames'].apply(lambda x: x.split(','))
    
    return jsonify(city.to_dict(orient='records'))


@app.route('/get_cities_list')
def get_cities_list():
    '''
    Returns a list with information about cities
    by page number and the number of cities displayed on the page
    '''
    
    page = request.args.get('page', default=1, type=int) - 1
    size = request.args.get('size', type=int)
    
    if not size or size <= 0 or page < 0:
        return {}
    else:
        s_index = page * size
        e_index = s_index + size
        cities = data[data['feature class'] == 'P'][s_index:e_index]

    return jsonify(cities.to_dict(orient='records'))


@app.route('/get_cities_by_name')
def get_cities_by_name():
    '''
    Returns information about two cities by their name (in Russian), and also additionally: 
    which of them is located to the north and whether they have the same time zone
    '''
    
    city_name1 = request.args.get('city_name1', type=str)
    city_name2 = request.args.get('city_name2', type=str)
    
    if not city_name1 or not city_name2:
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
    
    return jsonify(lst)


@app.route('/get_cities_names')
def get_cities_names():
    ''' Returns a hint with possible continuation options for city name '''
    
    city_name = request.args.get('city_name', type=str)
    
    cities = data[(data['alternatenames'].str.contains(city_name, na=False, case=False)) \
        & (data['feature class'] == 'P')].sort_values(by=['population'], ascending=False)
    cities['alternatenames'] = cities['alternatenames'].apply(lambda x: x.split(','))
    
    lst = []
    for city in cities['alternatenames']:
        for alternatename in city:
            if city_name.lower() in alternatename.lower() and alternatename not in lst\
                and re.search('[а-яА-ЯёЁ]', alternatename):
                lst.append(alternatename)

    return jsonify(lst)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
