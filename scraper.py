# scraper.py

import time
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import CONFIG


def create_session():
    """Создает сессию requests с настройками повторных попыток."""
    session = requests.Session()
    retry_strategy = Retry(
        total=CONFIG["max_retries"],
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def parse_books_page(soup: BeautifulSoup):
    """Парсит объект BeautifulSoup и возвращает список словарей с данными о книгах."""
    books = []
    articles = soup.find_all('article', class_='product_pod')

    for article in articles:
        # Название
        title_tag = article.find('h3').find('a')
        title = title_tag.get('title', 'N/A') if title_tag else 'N/A'

        # Цена
        price_tag = article.find('p', class_='price_color')
        price = price_tag.text.strip() if price_tag else 'N/A'

        # Наличие
        availability_tag = article.find('p', class_='instock availability')
        availability = availability_tag.text.strip() if availability_tag else 'N/A'

        # Рейтинг
        rating_tag = article.find('p', class_='star-rating')
        if rating_tag:
            rating_class = rating_tag.get('class', [])
            rating_word = next((cls for cls in rating_class if cls != 'star-rating'), 'N/A')
            rating = rating_word
        else:
            rating = 'N/A'

        books.append({
            'title': title,
            'price': price,
            'availability': availability,
            'rating': rating
        })

    return books


def scrape_all_books():
    """Основная функция для обхода всех страниц каталога и сбора данных."""
    session = create_session()
    all_books = []
    page_num = 1

    while True:
        if page_num == 1:
            url = f"{CONFIG['base_url']}page-1.html"
        else:
            url = f"{CONFIG['base_url']}page-{page_num}.html"

        print(f"Парсинг страницы: {url}")

        try:
            response = session.get(url, headers=CONFIG["headers"], timeout=CONFIG["timeout"])

            if response.status_code == 404:
                print("Достигнут конец каталога (404 Not Found).")
                break

            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            books_on_page = parse_books_page(soup)

            if not books_on_page:
                print("На странице не найдено книг. Завершение.")
                break

            all_books.extend(books_on_page)
            print(f"Собрано {len(books_on_page)} книг с этой страницы.")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}")
            break

        delay = random.uniform(*CONFIG["delay_range"])
        print(f"Ожидание {delay:.2f} секунд...")
        time.sleep(delay)

        page_num += 1

    return all_books


if __name__ == "__main__":
    print("Начало парсинга...")
    books_data = scrape_all_books()

    if not books_data:
        print("Не удалось собрать данные.")
    else:
        df = pd.DataFrame(books_data)
        print(f"\nПарсинг завершен. Собрано {len(df)} записей.")
        df.to_csv(CONFIG["output_csv"], index=False, encoding='utf-8-sig')
        print(f"Данные сохранены в файл: {CONFIG['output_csv']}")
