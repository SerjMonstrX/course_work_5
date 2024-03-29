import psycopg2


class DBManager:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        """Метод для подключения к БД"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to the database")
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def disconnect(self):
        """Метод для отключения от БД"""
        if self.conn:
            self.conn.close()
            print("Disconnected from the database")

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и количество вакансий у каждой компании"""
        result = []
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, COUNT(v.vac_id) AS vacancy_count
                    FROM Employers e
                    LEFT JOIN Vacancies v ON e.emp_id = v.employer_id
                    GROUP BY e.name;
                """)
                result = cur.fetchall()
        except psycopg2.Error as e:
            print(f"Error: {e}")
        return result

    def get_all_vacancies(self):
        """
        Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        result = []
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name AS company_name, v.name AS vacancy_name, 
                           CASE 
                               WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN 
                                   'Зарплата от: ' || v.salary_from::TEXT || ', Зарплата до: ' || v.salary_to::TEXT || ' ' || v.currency
                               WHEN v.salary_from IS NOT NULL THEN 
                                   'Зарплата от: ' || v.salary_from::TEXT || ' ' || v.currency
                               WHEN v.salary_to IS NOT NULL THEN 
                                   'Зарплата до: ' || v.salary_to::TEXT || ' ' || v.currency
                               ELSE 'Зарплата не указана' 
                           END AS salary_info,
                           v.currency,
                           v.url
                    FROM Employers e
                    JOIN Vacancies v ON e.emp_id = v.employer_id;
                """)
                result = cur.fetchall()
        except psycopg2.Error as e:
            print(f"Error: {e}")
        return result

    def get_avg_salary(self):
        """Метод получает среднюю зарплату по вакансиям"""
        result = None
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT ROUND(AVG((CAST(salary_from AS NUMERIC) + CAST(salary_to AS NUMERIC)) / 2)) AS average_salary
                    FROM Vacancies
                    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL AND currency = 'RUR';
                """)
                result = cur.fetchone()[0]
        except psycopg2.Error as e:
            print(f"Error: {e}")
        return result

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        result = []
        if avg_salary:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("""
                        SELECT e.name AS company_name, v.name AS vacancy_name, 
                               CASE 
                                   WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN 
                                       'Зарплата от: ' || v.salary_from::TEXT || ', Зарплата до: ' || v.salary_to::TEXT || ' ' || v.currency
                                   WHEN v.salary_from IS NOT NULL THEN 
                                       'Зарплата от: ' || v.salary_from::TEXT || ' ' || v.currency
                                   WHEN v.salary_to IS NOT NULL THEN 
                                       'Зарплата до: ' || v.salary_to::TEXT || ' ' || v.currency
                                   ELSE 'Зарплата не указана' 
                               END AS salary_info,
                               v.url
                        FROM Employers e
                        JOIN Vacancies v ON e.emp_id = v.employer_id
                        WHERE (v.salary_to > %s OR v.salary_from > %s) AND v.currency = 'RUR';
                    """, (avg_salary, avg_salary))
                    result = cur.fetchall()
            except psycopg2.Error as e:
                print(f"Error: {e}")
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        result = []
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name AS company_name, v.name AS vacancy_name, 
                           CASE 
                               WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN 
                                   'Зарплата от: ' || v.salary_from::TEXT || ', Зарплата до: ' || v.salary_to::TEXT || ' ' || v.currency
                               WHEN v.salary_from IS NOT NULL THEN 
                                   'Зарплата от: ' || v.salary_from::TEXT || ' ' || v.currency
                               WHEN v.salary_to IS NOT NULL THEN 
                                   'Зарплата до: ' || v.salary_to::TEXT || ' ' || v.currency
                               ELSE 'Зарплата не указана' 
                           END AS salary_info,
                           v.url
                    FROM Employers e
                    JOIN Vacancies v ON e.emp_id = v.employer_id
                    WHERE LOWER(v.name) LIKE %s;
                """, ('%' + keyword.lower() + '%',))
                result = cur.fetchall()
        except psycopg2.Error as e:
            print(f"Error: {e}")
        return result
