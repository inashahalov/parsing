# data_processor.py

import pandas as pd
import re
from config import CONFIG


def analyze_data(df: pd.DataFrame):
    """Проводит агрегацию и проверку данных."""
    print("\n--- Агрегация и проверка данных ---")
    print(f"Всего собрано книг: {len(df)}")

    print("\nУникальные рейтинги:")
    print(df['rating'].value_counts(dropna=False))

    print("\nПропущенные значения в каждом столбце:")
    print(df.isnull().sum())

    # Очистка и преобразование цены
    # Используем регулярное выражение для надежного извлечения числа
    df['price_numeric'] = df['price'].str.extract(r'(\d+\.\d+)')[0].astype(float)

    print("\nСтатистика по цене:")
    print(df['price_numeric'].describe())

    # Пример агрегации: средняя цена по рейтингу
    print("\nСредняя цена по рейтингу:")
    avg_price_by_rating = df.groupby('rating')['price_numeric'].mean().sort_values(ascending=False)
    print(avg_price_by_rating)


def load_and_process():
    """Загружает CSV и запускает анализ."""
    try:
        df = pd.read_csv(CONFIG["output_csv"], encoding='utf-8-sig')
        print(f"Данные загружены из {CONFIG['output_csv']}")
        analyze_data(df)
    except FileNotFoundError:
        print(f"Файл {CONFIG['output_csv']} не найден. Сначала запустите scraper.py")
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")


if __name__ == "__main__":
    load_and_process()
