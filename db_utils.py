import psycopg2
from psycopg2 import sql


def create_database(database_name: str, params: dict) -> None:
    """
    Создает новую базу данных.

    Args:
        database_name (str): Имя создаваемой базы данных.
        params (dict): Параметры подключения к PostgreSQL (host, user, password).

    Returns:
        None: Функция ничего не возвращает.
    """
    dsn = f"host={params['host']} user={params['user']} password={params['password']}"
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(database_name)))
        cursor.execute(
            sql.SQL("CREATE DATABASE {} TEMPLATE template0 ENCODING 'UTF8';").format(sql.Identifier(database_name))
        )
    finally:
        cursor.close()
        conn.close()


def create_tables(database_name: str, params: dict) -> None:
    """
    Создает таблицы employers и vacancies в указанной базе данных.

    Args:
        database_name (str): Имя базы данных.
        params (dict): Параметры подключения к PostgreSQL (host, user, password).

    Returns:
        None: Функция ничего не возвращает.
    """
    final_params = {**params, "database": database_name}

    with psycopg2.connect(**final_params) as conn:
        with conn.cursor() as cursor:
            # Создание таблицы employers
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS employers (
                    id SERIAL PRIMARY KEY,
                    employer_id INT UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(255)
                );
                """
            )

            # Создание таблицы vacancies с внешним ключом
            cursor.execute(
                """
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
                """
            )
        conn.commit()
