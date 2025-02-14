PORT ?= 8000

install:
	uv sync
check:
	uv run ruff check .
dev:
	uv run flask --debug --app page_analyzer.app:app run
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app
build:
	./build.sh
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app
fix:
	uv run ruff check --fix
