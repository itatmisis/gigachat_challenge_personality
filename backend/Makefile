PYTHON ?= .venv/bin/python
PYTHON_PRE ?= ../.venv/bin/python

install:
	python3.10 -m venv .venv
	. .venv/bin/activate
	$(PYTHON) -m pip install poetry
	poetry update

install-global:
	pip install poetry
	poetry update

run-web:
	cd app && $(PYTHON_PRE) -m poetry run python3 web_entrypoint.py

run-tg:
	cd app && $(PYTHON_PRE) -m poetry run python3 tg_bot_entrypoint.py

run-infra:
	docker compose up -d redis

run-docker:
	docker compose -d

test-integration:
	cd app && $(PYTHON_PRE) -m pytest -v -s

lint:
	pre-commit run -a

rebuild-backend:
	docker compose up -d --no-deps --build backend_web backend_tg

jup:
	. .venv/bin/activate
	$(PYTHON) -m jupyterlab

jup-darwin:
	. .venv/bin/activate
	$(PYTHON) -m jupyterlab --app-dir=/opt/homebrew/share/jupyter/lab
