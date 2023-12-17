from classes.dbmanager import *
from src.variables import *
# Подключение к БД
db_manager = DBManager(dbname='Headhunter', user='postgres', password=PGSQL_PASS)
db_manager.connect()


# Получение списка компаний и количества вакансий
companies_vacancies = db_manager.get_companies_and_vacancies_count()
print("\nКомпания и количество вакансий:")
print(companies_vacancies, end='\n\n')


# Получение всех вакансий с информацией
all_vacancies = db_manager.get_all_vacancies()
print("\nВсе вакансии:")
for vacancy in all_vacancies:
    print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, Зарплата до: {vacancy[3]}, Ссылка: {vacancy[4]}")


# Получение средней зарплаты
avg_salary = db_manager.get_avg_salary()
print(f"\nСредняя зарплата по вакансиям: {avg_salary} рублей")

# Получение вакансий с зарплатой выше средней
higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
print("\nВакансии с зарплатой выше среднего:")
for vacancy in higher_salary_vacancies:
    print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, Зарплата до: {vacancy[3]}, Ссылка: {vacancy[4]}")


# Получение вакансий по ключевому слову
vac_keyword = 'Директор'
keyword_vacancies = db_manager.get_vacancies_with_keyword(vac_keyword)
print(f"\nВакансии по ключевому слову {vac_keyword}")
print(keyword_vacancies)

# Отключение от БД
db_manager.disconnect()
