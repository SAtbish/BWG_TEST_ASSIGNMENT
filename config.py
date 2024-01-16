import os
from dotenv import load_dotenv

if not load_dotenv():
    print(
        "❗ Для корректной работы приложения необходим .env файл"
        "\n\nПуть до файла: ./<your_project>/.env"
        "\n\n📄 Структура файла 📄:"
        "\n# DB CONFIG"
        "\nDB_HOST={DB_HOST}"
        "\nDB_PORT={DB_PORT}"
        "\nDB_USER={DB_USER}"
        "\nDB_PSW={DB_PSW}"
        "\nDB_NAME={DB_NAME}"
        "\n\n# Redis CONFIG"
        "\nREDIS_HOST={REDIS_HOST}"
        "\nREDIS_PORT={REDIS_PORT}"
        "\nREDIS_DB={REDIS_DB}"
        "\n\n# BINANCE CONFIG"
        "\nBINANCE_API_KEY={BINANCE_API_KEY}"
        "\nBINANCE_API_SECRET={BINANCE_API_SECRET}"
    )

    exit(404)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PSW = os.getenv("DB_PSW")
DB_NAME = os.getenv("DB_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
