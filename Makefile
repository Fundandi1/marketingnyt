.PHONY: help setup run migrate superuser test lint format collectstatic clean

help:
	@echo "Available commands:"
	@echo "  setup        - Install dependencies and setup project"
	@echo "  run          - Run development server"
	@echo "  migrate      - Run database migrations"
	@echo "  superuser    - Create superuser"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  collectstatic - Collect static files"
	@echo "  clean        - Clean cache and temp files"

setup:
	poetry install
	cp .env.example .env
	poetry run python manage.py migrate
	@echo "Setup complete! Edit .env file and run 'make superuser' to create admin user"

run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

superuser:
	poetry run python manage.py createsuperuser

test:
	poetry run pytest

lint:
	poetry run ruff check .
	poetry run black --check .

format:
	poetry run ruff check --fix .
	poetry run black .

collectstatic:
	poetry run python manage.py collectstatic --noinput

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/
	rm -rf .pytest_cache/
