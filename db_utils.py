import psycopg2
from psycopg2 import sql

def create_database(database_name: str, params: dict):
    """Создает новую базу данных"""
    dsn = f"host={params['host']} user={params['user']} password={params['password']}"
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(database_name)))
    cursor.execute(sql.SQL("CREATE DATABASE {} TEMPLATE template0 ENCODING 'UTF8';").format(sql.Identifier(database_name)))
    cursor.close()
    conn.close()

def create_tables(database_name: str, params: dict):
    """Создает таблицы employers и vacancies"""
    final_params = {**params, "database": database_name}  # Используем "database" вместо "dbname"
    with psycopg2.connect(**final_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    id SERIAL PRIMARY KEY,
                    employer_id INT UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(255)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    vacancy_id INT UNIQUE NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    currency VARCHAR(10),
                    employer_id INT REFERENCES employers(employer_id),
                    url VARCHAR(255)
                );
            """)
        conn.commit()
        # conn.close()

# Пример использования:
# db_params = {
#     "host": "localhost",
#     "user": "postgres",
#     "password": "your_password"
# }
# create_database("hh_db", db_params)
# create_tables("hh_db", db_params)