### Getting started

###### started

### Доступные методы

###### get_city_by_geonameid()

Возвращает информацию о городе по его geonameid.

    http://127.0.0.1:8000/get_city_by_geonameid?geonameid=2013159

###### get_cities_list()

???

    http://127.0.0.1:8000/get_cities_list?

###### get_cities_by_name()

Возвращает информацию о двух городах по их названию (на русском языке), а также дополнительно: какой из них расположен севернее; находятся ли они в одном часовом поясе и разницу в часах.

Параметры case sensitive.

    http://127.0.0.1:8000/get_cities_by_name?city_name1=Москва&city_name2=Санкт-Петербург

###### get_cities_names()

Возвращает подсказку с возможными вариантами продолжения названия города.

Параметр case insensitive.

    http://127.0.0.1:8000/get_cities_names?city_name=москв

