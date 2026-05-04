.PHONY: core-build devcontainer-build


core-build:
	[ -f .env ] || touch .env
	docker compose build inky-agents-core

core-run:
	docker compose run inky-agents-core


devcontainer-build:
	docker compose -f .devcontainer/docker-compose.yml build inky-agents-devcontainer
