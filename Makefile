dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

dev-detached:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

down:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

down-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down

down-volumes:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v

logs:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

logs-once:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs

ps:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml ps

test:
	pytest