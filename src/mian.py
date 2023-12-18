import psycopg2
from classes.api import HeadhunterAPI
from variables import *

# Параметры подключения к БД
connection_params = {
    "host": "localhost",
    "database": "Headhunter",
    "user": "postgres",
    "password": PGSQL_PASS  # Замените на свой пароль
}

# SQL-запросы для создания таблиц
create_employers_table = """
    CREATE TABLE IF NOT EXISTS Employers (
        emp_id INTEGER PRIMARY KEY,
        name VARCHAR(255),
        site_url VARCHAR(255),
        hh_url VARCHAR(255),
        vacancies_url VARCHAR(255),
        open_vacancies INTEGER
    );
"""

create_vacancies_table = """
    CREATE TABLE IF NOT EXISTS Vacancies (
        vac_id INTEGER PRIMARY KEY,
        employer_id INTEGER REFERENCES Employers(emp_id),
        name VARCHAR(255),
        salary_from INTEGER,
        salary_to INTEGER,
        currency VARCHAR(50),
        url VARCHAR(255)
    );
"""

# SQL-запросы для удаления данных из таблиц, если они уже заполнены
truncate_employers_table = "TRUNCATE TABLE Employers CASCADE;"
truncate_vacancies_table = "TRUNCATE TABLE Vacancies CASCADE;"

# Получение данных от Headhunter API
hh_api = HeadhunterAPI(EMPLOYERS_ID_LIST)
hh_employers_data = hh_api.get_employers()
hh_vacancies_data = hh_api.get_vacancies()

try:
    # Подключение к БД и создание/очистка таблиц
    conn = psycopg2.connect(**connection_params)
    with conn.cursor() as cursor:
        cursor.execute(create_employers_table)
        cursor.execute(create_vacancies_table)

        # Очистка таблиц, если они уже существуют
        cursor.execute(truncate_employers_table)
        cursor.execute(truncate_vacancies_table)

        # Вставка данных о работодателях
        for employer in hh_employers_data:
            cursor.execute("""
                INSERT INTO Employers (emp_id, name, site_url, hh_url, vacancies_url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (emp_id) DO NOTHING;
            """, (
                employer['id'],
                employer['name'],
                employer['site_url'],
                employer['alternate_url'],
                employer['vacancies_url'],
                employer['open_vacancies']
            ))

        # Вставка данных о вакансиях
        for vacancy in hh_vacancies_data:
            for item in vacancy['items']:
                cursor.execute("""
                    INSERT INTO Vacancies (vac_id, employer_id, name, salary_from, salary_to, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vac_id) DO NOTHING;
                """, (
                    item['id'],
                    item['employer']['id'],
                    item.get('name'),
                    item['salary']['from'] if item.get('salary') else None,
                    item['salary']['to'] if item.get('salary') else None,
                    item['salary']['currency'] if item['salary'] and item['salary'].get('currency') else None,
                    item.get('url')
                ))

    conn.commit()
    print("Таблицы успешно созданы и заполнены")
except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
