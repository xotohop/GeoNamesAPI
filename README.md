# GeoNamesAPI

## Установка/Запуск

Код написан на Python 3.9

Если у Вас несколько версий Python, вместо

    python

используйте

PowerShell:
    
    py -3.9

Linux:
    
    python3.9

### Загрузка репозитория
    
    git clone https://github.com/xotohop/GeoNamesAPI.git
    cd GeoNamesAPI

### Файл с данными

Скачать архив и распаковать файл RU.txt в корне GeoNamesAPI:

    wget http://download.geonames.org/export/dump/RU.zip
    unzip RU.zip RU.txt

### virtualenv

Установка:

    python -m pip install virtualenv

Создание виртуальной среды:
    
    python -m venv venv

Запуск виртуальной среды

PowerShell:
    
    venv\Scripts\Activate.ps1 

Linux:
    
    . venv/bin/activate

### Установка зависимостей
    
    python -m pip install -r requirements.txt

### Запуск сервера
    
    python script.py

## Доступные методы

### GET /get_city_by_geonameid

Возвращает информацию о городе по его geonameid.

Пример:

    http://127.0.0.1:8000/get_city_by_geonameid?geonameid=2013159

### GET /get_cities_list

Возвращает список с информацией о городах по номеру страницы и количество городов, отображаемых на странице. Значение параметра "page" по умолчанию равно 1.

Пример:

    http://127.0.0.1:8000/get_cities_list?page=22&size=8
    http://127.0.0.1:8000/get_cities_list?size=1337

### GET /get_cities_by_name

Возвращает информацию о двух городах по их названию (на русском, с учетом регистра), а также дополнительно: какой из них расположен севернее; находятся ли они в одном часовом поясе и разницу в часах.

Пример:

    http://127.0.0.1:8000/get_cities_by_name?city_name1=Москва&city_name2=Санкт-Петербург

### GET /get_cities_names

Возвращает подсказку с возможными вариантами продолжения названия города.

Пример:

    http://127.0.0.1:8000/get_cities_names?city_name=москв

