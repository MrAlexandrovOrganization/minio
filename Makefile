ifneq ($(wildcard .retired),)
ifneq ($(filter up restart,$(MAKECMDGOALS)),)
$(error This source MinIO is retired; restore the latest data before reactivation)
endif
endif
DOCKER_COMPOSE_BASE = docker compose --project-directory "$(CURDIR)"
include makefiles/compose.mk
include makefiles/versions.mk
DOCKER_COMPOSE = docker compose --project-directory "$(CURDIR)" $(COMPOSE_FLAGS)

.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d --wait --wait-timeout 120

.PHONY: down
down:
	$(DOCKER_COMPOSE) down

.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

.PHONY: restart
restart:
	$(DOCKER_COMPOSE) restart minio

# Read-only validation of every tracked Compose combination, without runtime secrets.
.PHONY: compose-layout-check
compose-layout-check:
	$(DOCKER_COMPOSE_BASE) --env-file /dev/null -f compose/docker-compose.yml --profile '*' config --no-interpolate --no-env-resolution --quiet

check: compose-layout-check

versions:
	@$(foreach v,$(VERSION_VARS),printf '%s=%s\n' '$(v)' '$($(v))';)

.PHONY: compose
ARGS ?= ps
compose:
	$(DOCKER_COMPOSE) $(ARGS)
