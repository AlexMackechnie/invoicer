import os

config = {
    "local": {
        "ENV": "local",
        "SQLITE_PATH": os.getenv("SQLITE_PATH", ""),
        "GITLAB_CLIENT_ID": "32b37fe51705ab8b60136d4e94fc60204651d09d5eb994970db30b05bfc928d4",
        "GITLAB_CLIENT_SECRET": os.environ["GITLAB_CLIENT_SECRET"],
        "FLASK_APP_SECRET_KEY": os.environ["FLASK_APP_SECRET_KEY"]
    },
    "local-docker": {
        "ENV": "local-docker",
        "SQLITE_PATH": "/db/invoicer.db",
        "GITLAB_CLIENT_ID": "32b37fe51705ab8b60136d4e94fc60204651d09d5eb994970db30b05bfc928d4",
        "GITLAB_CLIENT_SECRET": os.environ["GITLAB_CLIENT_SECRET"],
        "FLASK_APP_SECRET_KEY": os.environ["FLASK_APP_SECRET_KEY"]
    },
    "prod": {
        "ENV": "prod",
        "SQLITE_PATH": "/db/invoicer.db",
        "GITLAB_CLIENT_ID": "32b37fe51705ab8b60136d4e94fc60204651d09d5eb994970db30b05bfc928d4",
        "GITLAB_CLIENT_SECRET": os.environ["GITLAB_CLIENT_SECRET"],
        "FLASK_APP_SECRET_KEY": os.environ["FLASK_APP_SECRET_KEY"]
    },
}
