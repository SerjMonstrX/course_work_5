import psycopg2
from classes.api import HeadhunterAPI
from variables import *

# Получение данных от Headhunter API
hh_api = HeadhunterAPI(EMPLOYERS_ID_LIST)
hh_employers_data = hh_api.get_employers()
hh_vacancies_data = hh_api.get_vacancies()

conn = psycopg2.connect(host='localhost', database='Headhunter', user='postgres', password=PGSQL_PASS)
try:
    with conn:
        with conn.cursor() as curr:
            # Вставка данных о работодателях
            for employer in hh_employers_data:
                curr.execute("""
                    INSERT INTO Employers (emp_id, name, site_url, hh_url, vacancies_url, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (emp_id) DO NOTHING;  -- Если работодатель уже существует, игнорируем вставку
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
                    curr.execute("""
                        INSERT INTO Vacancies (vac_id, employer_id, name, salary_from, salary_to, url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (vac_id) DO NOTHING;  -- Если вакансия уже существует, игнорируем вставку
                    """, (
                        item['id'],
                        item['employer']['id'],
                        item.get('name'),
                        item['salary']['from'] if item.get('salary') else None,
                        item['salary']['to'] if item.get('salary') else None,
                        item.get('url')
                    ))

except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    conn.close()