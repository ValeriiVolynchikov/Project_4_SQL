from hh_api import HH_API
from db_utils import create_database, create_tables
from db_manager import DBManager
import psycopg2

def insert_employers(data: list, conn):
    """Вставляет данные о работодателях в таблицу employers"""
    with conn.cursor() as cursor:
        for employer in data:
            cursor.execute("""
                INSERT INTO employers (employer_id, name, url)
                VALUES (%s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING;
            """, (employer["id"], employer["name"], employer["alternate_url"]))
    conn.commit()

def insert_vacancies(data: list, conn):
    """Вставляет данные о вакансиях в таблицу vacancies"""
    with conn.cursor() as cursor:
        for vacancy in data:
            cursor.execute("""
                INSERT INTO vacancies (vacancy_id, title, salary_from, salary_to, currency, employer_id, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vacancy_id) DO NOTHING;
            """, (
                vacancy["id"],
                vacancy["name"],
                vacancy["salary"]["from"] if vacancy.get("salary") else None,
                vacancy["salary"]["to"] if vacancy.get("salary") else None,
                vacancy["salary"]["currency"] if vacancy.get("salary") else None,
                vacancy["employer"]["id"],
                vacancy["alternate_url"]
            ))
    conn.commit()

def main():
    # Список ID компаний
    employer_ids = ["1942330",
    "49357",
    "3036416",
    "78638",
    "2748",
    "1740",
    "3529",
    "23427",
    "3772",
    "15478",
     "1122462"
    ]  # Добавьте IDs компаний

    # Создаем экземпляр API
    api = HH_API()

    # Подключаемся к БД
    db_params = {
        "host": "localhost",
        "user": "postgres",
        "password": "vvp162",
        "database": "hh_db"
    }

    # Создаем БД и таблицы
    create_database("hh_db", {**db_params, "database": "postgres"})
    create_tables("hh_db", db_params)

    # Получаем данные о компаниях и вакансиях
    employers_data = [api.get_employer(id) for id in employer_ids]
    vacancies_data = []
    for employer_id in employer_ids:
        vacancies_data.extend(api.get_vacancies(employer_id))

    # Вставляем данные в БД
    with psycopg2.connect(**db_params) as conn:
        insert_employers(employers_data, conn)
        insert_vacancies(vacancies_data, conn)

if __name__ == "__main__":
    main()
    print("Данные успешно загружены в БД")


def user_interface():
    db = DBManager({
        "host": "localhost",
        "user": "postgres",
        "password": "vvp162",
        "database": "hh_db"
    })

    while True:
        print("\nВыберите действие:")
        print("1. Компании и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            result = db.get_companies_and_vacancies_count()
            for row in result:
                print(f"Компания: {row[0]}, Вакансий: {row[1]}")
        elif choice == "2":
            result = db.get_all_vacancies()
            for row in result:
                print(f"Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}-{row[3]} {row[4]}, URL: {row[5]}")
        elif choice == "3":
            result = db.get_avg_salary()
            print(f"Средняя зарплата: {result[0][0]}")
        elif choice == "4":
            result = db.get_vacancies_with_higher_salary()
            for row in result:
                print(f"Вакансия: {row[0]}, Зарплата: {row[1]}")
        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            result = db.get_vacancies_with_keyword(keyword)
            for row in result:
                print(f"Вакансия: {row[0]}, Компания: {row[1]}, URL: {row[2]}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    user_interface()
