from enum import Enum


class EnvironmentVariablesTypes(Enum):
    """
    Environment variables types (used to access the DB, the API, etc).
    """

    # Main
    MASTER_KEY = "MASTER_KEY"
    WEBSERVER_PORT = "WEBSERVER_PORT"
    WEBSERVER_DEBUG = "WEBSERVER_DEBUG"
    # DB
    MONGODB_HOST = "MONGODB_HOST"
    MONGODB_PORT = "MONGODB_PORT"
    MONGODB_USERNAME = "MONGODB_USERNAME"
    MONGODB_PASSWORD = "MONGODB_PASSWORD"
    MONGODB_DB_NAME = "MONGODB_DB_NAME"
    MONGODB_AUTH_DB = "MONGODB_AUTH_DB"


class APIKeysTypes(Enum):
    """
    List of possible API key types.
    """

    SCANNER_NODE_REGISTRATION = "SCANNER_NODE_REGISTRATION"
    SCANNER_NODE_UNREGISTRATION = "SCANNER_NODE_UNREGISTRATION"
    STATUS_CHECKER = "STATUS_CHECKER"
