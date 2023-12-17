import re


def highlight_vacancy(func):
    def wrapper(vacancy_instance):
        print("=" * 40)
        func(vacancy_instance)
        print("=" * 40)
        print('')

    return wrapper


def remove_html_tags(text):
    if text:
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    else:
        return ''


class HeadhunterVacancies:

    def __init__(self, vacancy_data):
        self.__salary = (
            f"{'от ' if vacancy_data.get('salary') and vacancy_data['salary'].get('from') else ''}"
            f"{'' if not vacancy_data.get('salary') or not vacancy_data['salary'].get('from') else vacancy_data['salary']['from']}"
            f"{' до ' if vacancy_data.get('salary') and vacancy_data['salary'].get('to') else ''}"
            f"{'' if not vacancy_data.get('salary') or not vacancy_data['salary'].get('to') else vacancy_data['salary']['to']} "
            f"{vacancy_data['salary']['currency'] if vacancy_data.get('salary') else ''}"
        )
        self.__name = vacancy_data.get('name', '')
        self.__vacancy_url = vacancy_data.get('alternate_url', '')
        self.__requirement = vacancy_data.get('snippet', {}).get('requirement', 'Не указаны, подробнее смотрите описание вакансии на сайте.')

    def get_name(self):
        return self.__name

    def get_vacancy_url(self):
        return self.__vacancy_url

    def get_salary(self):
        return self.__salary

    def get_requirement(self):
        return self.__requirement

    @highlight_vacancy
    def display(self):
        print(f"Название вакансии: {self.__name}")
        print(f"Зарплата: {self.__salary}")
        print(f"Ссылка на вакансию: {self.__vacancy_url}")
        print(f"Требования: {remove_html_tags(self.__requirement)}")

