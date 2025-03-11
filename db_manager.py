import psycopg2

class DBManager:
    """Класс для управления данными в БД"""

    def __init__(self, params: dict):
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой"""
        query = """
            SELECT e.name, COUNT(v.id) AS vacancy_count
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name;
        """
        return self._execute_query(query)

    def get_all_vacancies(self):
        """Получает список всех вакансий"""
        query = """
            SELECT e.name AS employer_name, v.title, v.salary_from, v.salary_to, v.currency, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id;
        """
        return self._execute_query(query)

    def get_avg_salary(self):
        """Получает среднюю зарплату"""
        query = """
            SELECT AVG((salary_from + salary_to) / 2) AS avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """
        return self._execute_query(query)

    def get_vacancies_with_higher_salary(self):
        """Получает вакансии с зарплатой выше средней"""
        query = """
            SELECT title, (salary_from + salary_to) / 2 AS avg_salary
            FROM vacancies
            WHERE (salary_from + salary_to) / 2 > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancies)
            AND salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """
        return self._execute_query(query)

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает вакансии с указанным ключевым словом"""
        query = f"""
            SELECT title, employer_id, url
            FROM vacancies
            WHERE title ILIKE '%{keyword}%';
        """
        return self._execute_query(query)

    def _execute_query(self, query: str):
        """Выполняет SQL-запрос и возвращает результат"""
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

# Пример использования:
# db = DBManager({
#     "host": "localhost",
#     "user": "postgres",
#     "password": "your_password",
#     "dbname": "hh_db"
# })
# print(db.get_companies_and_vacancies_count())