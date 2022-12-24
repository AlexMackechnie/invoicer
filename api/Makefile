.PHONY: install-build-tools freeze freeze-upgrade freeze-dev freeze-dev-upgrade build deactivate

# ------------------------------- #
# Tools                           #
# ------------------------------- #

upgrade_pip:
	pip install --upgrade pip

# ------------------------------- #
# Build Environment               #
# ------------------------------- #

# Installing Build Tools

install-build-tools: upgrade_pip
	pip install --upgrade build wheel pip-tools

clean:
	pip uninstall reference-app -y
	pip freeze | xargs pip uninstall -y
	rm -rf build
	find . -type d -name "__pycache__" -exec rm -rf {} \;
	find . -type d -name "*.egg-info" -exec rm -rf {} \;

# Freezing Dependencies

freeze: install-build-tools
	python -m piptools compile -o requirements.txt pyproject.toml

freeze-upgrade: install-build-tools
	python -m piptools compile -o requirements.txt --upgrade pyproject.toml

freeze-dev: install-build-tools
	python -m piptools compile --extra dev -o requirements-dev.txt pyproject.toml

freeze-dev-upgrade: install-build-tools
	python -m piptools compile --extra dev -o requirements-dev.txt --upgrade pyproject.toml

# ------------------------------- #
# Dev Execution Environment       #
# ------------------------------- #

install-dev: upgrade_pip requirements.txt requirements-dev.txt pyproject.toml
	pip install -r requirements.txt --compile
	pip install -r requirements-dev.txt --compile
	pip install -e . --no-deps --config-settings editable_mode=strict

run-dev:
	nohup python -m flask --app invoicer_api.app run --port 5001 &

stop-dev:
	pkill -f "flask --app invoicer_api.app run"
