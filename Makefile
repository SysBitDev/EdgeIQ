# Makefile
PY_BLACK ?= $(shell command -v black 2>/dev/null)
PY_RUFF  ?= $(shell command -v ruff  2>/dev/null)

# Якщо раптом немає у PATH (наприклад, стара сесія) — спроба явного шляху
ifeq ($(PY_BLACK),)
  PY_BLACK := $(HOME)/.local/bin/black
endif
ifeq ($(PY_RUFF),)
  PY_RUFF := $(HOME)/.local/bin/ruff
endif

.PHONY: dev up down fmt lint test

dev:
	cd devops && docker compose up --build

up:
	cd devops && docker compose up -d --build

down:
	cd devops && docker compose down

fmt:
	@echo "Using BLACK: $(PY_BLACK)"
	@echo "Using RUFF : $(PY_RUFF)"
	"$(PY_BLACK)" backend
	"$(PY_RUFF)" check backend --fix || true
	# фронт-формат (за потреби)
	npm --prefix frontend i --silent || true
	npx --prefix frontend prettier -w "frontend/**/*.{js,jsx,json,css,md}" || true

lint:
	"$(PY_RUFF)" check backend
	npm --prefix frontend i --silent || true
	npx --prefix frontend eslint "frontend/src/**/*.{js,jsx}" || true

test:
	@echo "no tests yet"
