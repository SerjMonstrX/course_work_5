import requests


class HeadhunterAPI:
    """ Класс для работы с API Headhunter """

    def __init__(self, employer_ids=None, page=0):
        self.params = {"page": page}
        self.employer_ids = employer_ids or []

    def get_employers(self):
        """Получение данных о работодателях с сайта HH по API для заданных ID."""

        all_employers_data = []
        for employer_id in self.employer_ids:
            company_url = f"https://api.hh.ru/employers/{employer_id}"
            try:
                response = requests.get(company_url)
                response.raise_for_status()
                employers_data = response.json()
                all_employers_data.append(employers_data)
            except requests.RequestException as e:
                print(f'Ошибка {response.status_code}: {response.text}')
                raise RuntimeError(f"Не удалось получить данные о работодателе с ID {employer_id}: {str(e)}")
        return all_employers_data

    def get_vacancies(self):
        """Получение данных о вакансиях работодателей с сайта HH по API для заданных ID."""

        all_vacancies_data = []
        for employer_id in self.employer_ids:
            vacancies_url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
            try:
                response = requests.get(vacancies_url)
                response.raise_for_status()
                vacancies_data = response.json()
                all_vacancies_data.append(vacancies_data)
            except requests.RequestException as e:
                print(f'Ошибка {response.status_code}: {response.text}')
                raise RuntimeError(f"Не удалось получить данные о вакансиях работодателя с ID {employer_id}: {str(e)}")
        return all_vacancies_data
