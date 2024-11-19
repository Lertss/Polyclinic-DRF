# Имя файла конфигурации для Docker Compose
COMPOSE_FILE = docker-compose.yml

# Путь к файлу переменных окружения
ENV_FILE = env_file/.env.postgres

# Команда для запуска контейнеров в фоновом режиме
up:
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up -d

# Команда для остановки контейнеров
down:
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) down

# Команда для перезапуска контейнеров
restart: down up

# Команда для просмотра статуса контейнеров
status:
	docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) ps
