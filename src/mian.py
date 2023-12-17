import psycopg2
import json
from classes.jsonhandler import HeadhunterJson
from classes.api import HeadhunterAPI
from variables import *

hh_api = HeadhunterAPI(EMPLOYERS_ID_LIST)
hh_employers_data = hh_api.get_employers()
hh_vacancies_data = hh_api.get_vacancies()
for vacancy in hh_vacancies_data:
    print(vacancy.get('name'))
# Преобразование полученных данных в формат JSON с отступами для красивого вывода
formatted_data = json.dumps(hh_vacancies_data, indent=4, ensure_ascii=False)

json_company_data = HeadhunterJson()
json_vacancies_data = HeadhunterJson(filename='hh_vacancies_data.json')

json_company_data.save_to_json(hh_employers_data)
json_vacancies_data.save_to_json(hh_vacancies_data)

"""----------------------------------------------------"""


conn = psycopg2.connect(host='localhost', database='Headhunter', user='postgres', password=PGSQL_PASS)
try:
    with conn:
        with conn.cursor() as curr:
            hh_api = HeadhunterAPI(EMPLOYERS_ID_LIST)
            employers_data = hh_api.get_employers()
            vacancies_data = hh_api.get_vacancies()
            for employer in employers_data:
                curr.execute("""
                    INSERT INTO Employers (emp_id, name, site_url, hh_url, vacancies_url, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    employer['id'],
                    employer['name'],
                    employer['site_url'],
                    employer['alternate_url'],
                    employer['vacancies_url'],
                    employer['open_vacancies']
                ))
                employer_id = curr.fetchone()[0]

                for vacancy in vacancies_data[1]['items']:

                    curr.execute("""
                        INSERT INTO Vacancies (vac_id, employer_id, name, salary_from, salary_to, url)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (
                        vacancy['id'],
                        vacancy['employer']['id'],
                        vacancy.get('name'),
                        vacancy['salary']['from'] if vacancy.get('salary') else None,
                        vacancy['salary']['to'] if vacancy.get('salary') else None,
                        vacancy.get('url')
                    ))

except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    conn.close()
