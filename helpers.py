import pandas as pd
from datetime import datetime
from pytz import timezone

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
