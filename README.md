# minio

## Структура Compose

Файлы Docker Compose находятся в `compose/`; основной файл — `compose/docker-compose.yml`.
Команды запускайте из корня проекта через Makefile: он задаёт `--project-directory`
на корень checkout. Build contexts, bind mounts, `env_file` и секреты остаются
относительными к этому корню; имена Compose project, сервисов, сетей и томов сохранены.
При явном вызове Docker используйте `docker compose --project-directory . -f compose/docker-compose.yml ...`.
Если в приватной `.env` или окружении задан `COMPOSE_FILE`, добавьте `compose/`
к прежним именам файлов, сохранив прежний набор overlays и порядок. Для плавного
перехода Make также распознаёт прежние короткие имена, если файлы уже перенесены.
Не меняйте project name и не удаляйте прежние тома для переноса файлов.

## Stash storage migration

MinIO for Stash now runs on ASUS with the same named volume, credentials and
release. The source remains stopped with restart=no; preserve its volume for
rollback. Transfer the full cold volume, including .minio.sys, and verify every
file hash before activation. The private off-VM archive is alongside the Stash
PostgreSQL backup under ~/.local/state/server-migration-20261020 on the Mac.
Version pin: makefiles/versions.mk; make versions displays it.
