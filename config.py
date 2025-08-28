# config.py

CONFIG = {
    "base_url": "http://books.toscrape.com/catalogue/",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    },
    "delay_range": (1, 2),  # Задержка между запросами от 1 до 2 секунд
    "max_retries": 3,       # Максимальное количество повторных попыток
    "timeout": 10,          # Таймаут для запроса в секундах
    "output_csv": "scraped_books.csv",
    "db_config": {
         "dbname": "myproject_db",
         "user": "postgres",
         "password": "my_secure_password",
         "host": "localhost",
         "port": "5432"
    }
}
