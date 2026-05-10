dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

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

ps:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml ps

test:
	pytest