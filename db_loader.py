# db_loader.py

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from config import CONFIG

def load_to_db():
    """Загружает данные в PostgreSQL."""
    try:
        df = pd.read_csv(CONFIG["output_csv"], encoding='utf-8-sig')
        print(f"Данные загружены из {CONFIG['output_csv']}")

        conn = psycopg2.connect(**CONFIG["db_config"])
        cur = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT,
            price TEXT,
            availability TEXT,
            rating TEXT
        );
        """
        cur.execute(create_table_query)

        # Подготавливаем данные
        # Заменяем NaN на None для корректной вставки в БД
        df_clean = df.where(pd.notnull(df), None)
        data_tuples = [tuple(row) for row in df_clean[['title', 'price', 'availability', 'rating']].values]

        insert_query = """
        INSERT INTO books (title, price, availability, rating) VALUES %s
        """
        execute_values(cur, insert_query, data_tuples)

        conn.commit()
        print(f"Успешно загружено {len(data_tuples)} записей в БД.")

    except Exception as e:
        print(f"Ошибка при загрузке в БД: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    load_to_db()
