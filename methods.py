import pandas as pd
import re
from flask import Flask, request, jsonify

from helpers import cities_cleaner, north, tz_diff

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


@app.route('/')
@app.route('/index')
def index():
    return '''
<html>
    <head>
        <title>InfoTeCS test task</title>
    </head>
    <body>
        <h3>Доступные методы:</h3>
        <h3>get_city_by_geonameid</h3>
        <p>http://127.0.0.1:8000/get_city_by_geonameid?geonameid=<b>2013159</b></p>
        <h3>get_cities_list</h3>
        <p>http://127.0.0.1:8000/get_cities_list?</p>
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
    '''  '''
    
    pass


@app.route('/get_cities_by_name')
def get_cities_by_name():
    '''
    Returns information about two cities by their name (in Russian), and also additionally: 
    which of them is located to the north and whether they have the same time zone
    '''
    
    city_name1 = request.args.get('city_name1', type=str)
    city_name2 = request.args.get('city_name2', type=str)
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
