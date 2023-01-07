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

# Build Wheel
build: install-build-tools
	python -m build

# ------------------------------- #
# Run Locally outside Docker      #
# ------------------------------- #

install-dev: upgrade_pip requirements.txt requirements-dev.txt pyproject.toml
	pip install -r requirements.txt --compile
	pip install -r requirements-dev.txt --compile
	pip install -e . --no-deps --config-settings editable_mode=strict

run-local:
	ENV=local nohup python -u -m flask --app invoicer_api.app run --port 5001 &

stop-local:
	pkill -f "flask --app invoicer_api.app run"

# ------------------------------- #
# Build Image                     #
# ------------------------------- #

build-docker: build
	docker build -t invoicer .

clean-docker:
	rm -rf build dist
	docker container stop invoicer || true
	docker image rm -f invoicer || true

# ------------------------------- #
# Run Locally inside Docker       #
# ------------------------------- #

run-local-docker:
	docker run \
		--rm -d \
		-p 5001:5001 \
		-v ${SQLITE_PATH}:/db/invoicer.db \
		-e ENV="local-docker" \
		-e FLASK_APP_SECRET_KEY=${FLASK_APP_SECRET_KEY} \
		-e GITLAB_CLIENT_SECRET=${GITLAB_CLIENT_SECRET} \
		--name invoicer \
		invoicer

stop-local-docker:
	docker container stop invoicer

# ------------------------------- #
# Run in Prod inside Docker       #
# ------------------------------- #

run-prod-docker:
	docker run \
		--rm -d \
		-p 5001:5001 \
		-v /db/invoicer.db:/db/invoicer.db \
		-v ${SSL_CERT_PATH}:/ssl/fullchain.pem \
		-v ${SSL_KEY_PATH}:/ssl/privkey.pem \
		-e ENV="prod" \
		-e FLASK_APP_SECRET_KEY=${FLASK_APP_SECRET_KEY} \
		-e GITLAB_CLIENT_SECRET=${GITLAB_CLIENT_SECRET} \
		--name invoicer \
		ghcr.io/alexmackechnie/invoicer:1673040893

