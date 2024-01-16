# BWG_TEST_ASSIGNMENT
Это тестовое задание для компании [**"Black wall group"**](https://blackwallgroup.ru/).

## Содержание
- [Задание](#Задание)
- [Технологии](#Технологии)
- [Первый запуск](#первый-запуск)
- [FAQ](#faq-)

## Задание
**Результат**: роут, по которому можно получать курсы с биржи binance. Требуются курсы за текущий момент времени. 
**Реализация**: нужен воркер, который получает курсы по апи бинанса и хранит у себя эти данные. По роуту можно получить курсы либо по всем валютным парам, либо одну конкретную. 
**Стек**: Python (FastApi), Postgres, Redis (при желании)

## Технологии
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [FastApi](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Poetry](https://python-poetry.org/)
- [python-binance](https://python-binance.readthedocs.io/en/latest/)
- [Redis](https://redis.io/)
- [yoyo](https://pypi.org/project/yoyo-migrations/)

## Первый запуск

Прежде всего необходимо добавить файл окружения .env
Он имеет следующую структуру:
```text
DB_HOST=...
DB_PORT=...
DB_USER=...
DB_PSW=...
DB_NAME=...

REDIS_DB=...
REDIS_NOTIFICATIONS_KEY=...
REDISMAXPULL=...

BINANCE_API_KEY=...
BINANCE_API_SECRET=...
```

Как получить ключ от BINANCE_API_KEY и BINANCE_API_SECRET читаем [тут](https://www.binance.com/en/my/settings/api-management).

Развернём проект с помощью [pyenv и poetry](https://habr.com/ru/articles/599441/)

Установим зависимости:
```commandline
poetry init
```
Зайдём в виртуальное окружение с помощью команды:
```commandline
poetry shell
```
Запустим файл main.py
```commandline
python main.py
```
Для проверки работоспособности обратитесь к swagger-у проекта по адресу: http://127.0.0.1:8000/docs

### Docker
Добавим файл окружения .docker_env
```text
REDIS_DB=...
REDIS_NOTIFICATIONS_KEY=...
REDISMAXPULL=...

DB_PORT=...
DB_HOST=...
DB_PSW=...
DB_NAME=...
DB_USER=...
POSTGRES_PASSWORD=...
POSTGRES_USER=...
POSTGRES_DB=...

BINANCE_API_KEY=...
BINANCE_API_SECRET=...
```

Сначала необходимо собрать билд проекта.
```commandline
docker compose build
```
Далее следует его запустить.
```commandline
docker compose up
```
Проверяем доступность сервиса по обращению к swagger-у: http://127.0.0.1:9090/docs

## FAQ 
- Реализовал 6 роутов:
  - `/symbols/get/all` для записи в базу данных всех валютных пар.
  - `/symbols/get/{symbol}` для записи в базу данных определённой валютной пары.
  - `/get/{symbol}/history` для получения истории из базы данных по определённой валютной паре.
  - `/get/{symbol}/history/paginated` для получения истории из базы данных по определённой валютной паре с пагинацией.
  - `/get/{symbol}/last` для получения последней записи определённой валютной пары из базы данных.
  - `/` и `/ping` для проверки доступности работы приложения.
- Добился скорости записи в базу данных **2438** элементов за ≈ **0.09** секунд **(10600/сек)** за счёт 
  асинхронности и отдельного метода для записи сразу большого количества данных.
- Также с помощью использования **Websocket**-ов добился ускорения получения данных от апи бинанса до **0.27** секунд.
- Использовал паттерн **UnitOfWork**.
- Добавил миграции **Alembic** и **yoyo-migrations**. 
- Использовал асинхронные клиенты для работы с базой данных **postgresql** и **BinanceAPI**.
- Асинхронный **FastAPI**.
- Использовал **Redis** для кэширования.
