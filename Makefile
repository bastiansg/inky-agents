.PHONY: core-build devcontainer-build


core-build:
	[ -f .env ] || touch .env
	docker compose build inky-agents-core

core-run:
	docker compose run inky-agents-core


devcontainer-build: core-build
	docker compose -f .devcontainer/docker-compose.yml build inky-agents-devcontainer


mongo-start:
	docker compose up -d inky-agents-mongo

mongo-stop:
	docker compose stop inky-agents-mongo

mongo-restart: mongo-stop mongo-start


app-build: core-build
	docker compose build inky-agents-app

app-run: app-build
	docker compose  run --rm inky-agents-app

app-up: app-build
	docker compose up -d inky-agents-app

app-stop:
	docker stop inky-agents-app

app-restart: app-stop app-up
