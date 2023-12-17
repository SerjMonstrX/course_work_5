import json
from abc import ABC, abstractmethod


class JsonHandler(ABC):

    @abstractmethod
    def save_to_json(self, vacancies_data):
        pass

    @abstractmethod
    def load_from_json(self):
        pass


class HeadhunterJson(JsonHandler):

    def __init__(self, filename='hh_employers_data.json'):
        self.filename = filename

    def save_to_json(self, employers_data):
        """ Функция для сохранения данных в JSON файл"""

        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(employers_data, file, ensure_ascii=False, indent=2)
            print(f"Вакансии успешно сохранены в файл {self.filename}")
        except IOError as e:
            raise RuntimeError(f"Ошибка при записи вакансий в JSON: {str(e)}")

    def load_from_json(self):
        """ Функция для загрузки данных из JSON файла"""

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                vacancies_data = json.load(file)
            return vacancies_data
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Ошибка при чтении вакансий из JSON: {str(e)}")


    def load_from_json_sorted_by_salary(self):
        """ Функция для загрузки данных из JSON файла с сортировкой по зарплате"""

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                vacancies_data = json.load(file)
                # Фильтром удаляем вакансии без указания зарплаты
                filtered_vacancies_data = [vacancy for vacancy in vacancies_data if vacancy.get('salary', {})
                                        and isinstance(vacancy['salary'].get('from'), int)]
                # Сортируем отфильтрованный список вакансий по убыванию зарплаты
                sorted_vacancies_data = sorted(filtered_vacancies_data,
                                        key=lambda x: x.get('salary', {}).get('from', float('inf')), reverse=True)

            return sorted_vacancies_data
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Ошибка при чтении вакансий из JSON: {str(e)}")