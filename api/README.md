# Invoicer

### Running Locally without Container

To run:
```bash
# Environment Variables 
export ENV=local
export SQLITE_PATH=<full-path-to-.db-file>
export FLASK_APP_SECRET_KEY=<flask-secret>
export GITLAB_CLIENT_SECRET=<secret-for-gitlab-oauth>

# Build and Run
make install-dev
make run-local
```

### Running Locally inside Container

```bash
# Environment Variables 
export ENV=local-docker
export SQLITE_PATH=<full-path-to-.db-file>
export FLASK_APP_SECRET_KEY=<flask-secret>
export GITLAB_CLIENT_SECRET=<secret-for-gitlab-oauth>

# Build and Run
make docker-build
make run-docker-local
```
