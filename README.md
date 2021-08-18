# GeoNames API

## Установка/Запуск

Код написан на Python 3.9.6

Если у Вас несколько версий Python, вместо

    python

используйте

PowerShell:
    
    py -3.9

Linux:
    
    python3.9

### Загрузка репозитория
    
    git clone https://github.com/xotohop/geo_test_task.git
    cd geo_test_task

### Файл с данными

Скопировать файл RU.txt из архива в корень папки geo_test_task

    http://download.geonames.org/export/dump/RU.zip

### virtualenv

Установка:

    python -m pip install virtualenv

Создание виртуальной среды:
    
    python -m venv venv

Запуск виртуальной среды

PowerShell:
    
    venv\Scripts\Activate.ps1 

Linux:
    
    ./venv/bin/activate

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

???

Пример:

    http://127.0.0.1:8000/get_cities_list?

### GET /get_cities_by_name

Возвращает информацию о двух городах по их названию (на русском языке), а также дополнительно: какой из них расположен севернее; находятся ли они в одном часовом поясе и разницу в часах. Параметры чувствительны к регистру.

Пример:

    http://127.0.0.1:8000/get_cities_by_name?city_name1=Москва&city_name2=Санкт-Петербург

### GET /get_cities_names

Возвращает подсказку с возможными вариантами продолжения названия города. Параметр не чувствителен к регистру.

Пример:

    http://127.0.0.1:8000/get_cities_names?city_name=москв

