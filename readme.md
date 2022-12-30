Подготовка данных для анализа рынка акций/валют по данным временных рядов через api от www.alphavantage.co

Стэк:
    БД: postgres
    ORM: SQLAlchemy + pydantic
    DB Migrations: alembic

#####################################################
Структура:

|\alembic\              - настройка миграций
|\finance_parser\       - основной модуль
|-\crud\                - работа с бд
|-\config.py            - настройки
|-\models.py            - модели данных
|-\schemas.py           - схемы ввода данных
|-\utils.py             - доп.функции
|\get_intial_data.py    - первоначальная загрузка данных
|\get_yesterday_data.py - дозагрузка вчерашних данных

#####################################################

Использование:

1) Создание базы данных

    #sudo su - postgres
    #createuser finance_user
    #createdb finance_db
    #psql
    $alter user finance_user with encrypted password 'finance_pass';
    $grant all privileges on database finance_db to finance_user;

2) Создание таблиц БД с помощью миграций

    #python -m alembic revision --autogenerate -m "initial"
    #python -m alembic upgrade head 

3) первоначальная загрузка данных

    python get_initial_data.py

4) установка задания для пополнения данных

    #crontab -e

    добавить в конец файла:

    0   1  *   *   * /...path_to_project.../get_yesterday_data.py