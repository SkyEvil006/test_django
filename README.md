# Сервис выплат (Payout Service)

REST API приложение на Django для управления заявками на выплату средств с асинхронной обработкой.

## Стек

- **Backend:** Django 4.2 + Django REST Framework
- **Асинхронная обработка:** Celery + Redis
- **База данных:** PostgreSQL
- **Управление зависимостями:** Poetry
- **Контейнеризация:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Качество кода:** Black, Ruff, mypy
- **API документация:** Swagger/Redoc (drf-spectacular)

## Архитектура

Проект использует многослойную архитектуру:
- **Models** — описание данных
- **Serializers** — валидация и преобразование данных
- **Views** — обработка HTTP запросов
- **Services** — бизнес-логика
- **Repositories** — работа с базой данных
- **Tasks** — асинхронные задачи Celery

## Быстрый старт (Poetry)

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
# в отдельном терминале
poetry run celery -A payouts worker --loglevel=info
```

Тесты:

```bash
poetry run pytest
```

Те же команды доступны через Makefile: `make migrate`, `make runserver`, `make celery-worker`, `make test`, `make lint`, `make format`, `make docker-up`, `make docker-down`.

## Docker

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
```

Endpoints:
- API — http://localhost:8000/api/v1/payouts/
- Swagger — http://localhost:8000/api/docs/

## API

- `GET /api/v1/payouts/` — список заявок
- `POST /api/v1/payouts/` — создание (старт Celery-задачи)
- `GET /api/v1/payouts/{id}/` — детали
- `PATCH /api/v1/payouts/{id}/` — обновление статуса
- `DELETE /api/v1/payouts/{id}/` — удаление

Цикл обработки: `pending → processing → completed/failed` (2-секундная имитация, случайный финал).

## Production

**Компоненты:** Django (Gunicorn), PostgreSQL, Redis, Celery workers.

**Шаги:**
1. `poetry install --only main`
2. Настроить переменные окружения (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `POSTGRES_*`, `CELERY_*`)
3. `python manage.py migrate` (+ `collectstatic` при необходимости)
4. Запустить Gunicorn и Celery workers (systemd/supervisor/k8s)
5. Поверх — балансировщик, Pgbouncer, мониторинг (Flower/Prometheus) по потребности.

**Docker:** `docker build -t payout-service .` и запуск контейнера с теми же переменными окружения.

## Переменные окружения

| Переменная | Назначение | Значение по умолчанию |
|-----------|------------|------------------------|
| `DJANGO_SECRET_KEY` | секретный ключ | обязательно в prod |
| `DJANGO_DEBUG` | режим отладки | `True` |
| `POSTGRES_DB/USER/PASSWORD/HOST/PORT` | параметры БД | `payout_db` / `payout_user` / `payout_pass` / `localhost` / `5432` |
| `CELERY_BROKER_URL` | Redis | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | backend результатов | `redis://localhost:6379/0` |