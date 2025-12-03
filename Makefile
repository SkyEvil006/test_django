.PHONY: help install migrate runserver test celery-worker \
        lint format docker-up docker-down clean

POETRY ?= poetry
PYTHON ?= $(POETRY) run python
DOCKER_COMPOSE ?= docker-compose

help: ## Показать справку по командам
	@echo 'Использование: make [команда]'
	@echo ''
	@echo 'Доступные команды:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Установка
install: ## Установить зависимости (production + dev)
	$(POETRY) install

install-prod: ## Установить только production зависимости
	$(POETRY) install --only main

# Django
migrate: ## Применить миграции БД
	$(PYTHON) manage.py migrate

runserver: ## Запустить Django сервер
	$(PYTHON) manage.py runserver

# Celery
celery-worker: ## Запустить Celery worker
	$(POETRY) run celery -A payouts worker --loglevel=info

# Тестирование
test: ## Запустить тесты
	$(POETRY) run pytest

# Качество кода
format: ## Отформатировать код (Black)
	$(POETRY) run black .

lint: ## Проверить код линтерами
	@echo "Проверка Black..."
	@$(POETRY) run black --check .
	@echo "Проверка Ruff..."
	@$(POETRY) run ruff check .
	@echo "Проверка mypy..."
	@$(POETRY) run mypy payouts conf --ignore-missing-imports || true

# Docker
docker-up: ## Запустить все сервисы в Docker
	$(DOCKER_COMPOSE) up -d
	@sleep 3
	$(DOCKER_COMPOSE) exec web python manage.py migrate
	@echo "\nСервисы запущены!"
	@echo "API: http://localhost:8000/api/v1/payouts/"
	@echo "Swagger: http://localhost:8000/api/docs/"

docker-down: ## Остановить Docker сервисы
	$(DOCKER_COMPOSE) down

# Очистка
clean: ## Очистить временные файлы
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
