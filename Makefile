SHELL=/bin/bash

.PHONY: help
help:
	@echo ""
	@echo "Usage: make COMMAND"
	@echo ""
	@echo "VyOS Collection Makefile"
	@echo ""
	@echo "Commands:"
	@echo ""
	@echo "  lint              Lint project with ansible-lint"
	@echo ""

.PHONY: lint
lint:
	@docker run \
	--rm \
	-it \
	--pull always \
	--network host \
	-e PUID=$$(id -u) \
	-e PGID=$$(id -g) \
	--mount type=bind,source=".",target=/app \
	ghcr.io/gamersoutreach/ansible-runner:latest \
	ansible-lint
