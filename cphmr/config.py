# MARK: - Libraries
import os
import sys

from dotenv import load_dotenv

from cphmr.typesa import EnvironmentVariablesTypes


# MARK: - .env Loader
load_dotenv()


# MARK: - Environment Variables
def checkEnvironment() -> None:
    """
    Checks if there are needed environment variables according\
    to the `typesa.EnvironmentVariablesTypes`.

    Returns nothing, but raises an exception if there are missing environment variables.
    """
    try:
        for value in EnvironmentVariablesTypes.__members__.values():
            _ = os.environ[value.name]
    except KeyError:
        print("One or more required environment variables are not set.")
        sys.exit(1)


# MARK: - Configurations for environment variables
class Config:
    """
    A better getter for environment variables.

    Returns the value of the environment variable with the given name according\
    to the `typesa.EnvironmentVariablesTypes` (+ given `classmethod`s) and\
    pretermined type.
    """

    @classmethod
    def getMongoDBURI(cls) -> str:
        """
        Returns the MongoDB URI in string format.
        """
        return f"mongodb://\
{os.environ[EnvironmentVariablesTypes.MONGODB_USERNAME.value]}:\
{os.environ[EnvironmentVariablesTypes.MONGODB_PASSWORD.value]}@\
{os.environ[EnvironmentVariablesTypes.MONGODB_HOST.value]}:\
{os.environ[EnvironmentVariablesTypes.MONGODB_PORT.value]}/?authSource=\
{os.environ[EnvironmentVariablesTypes.MONGODB_AUTH_DB.value]}"

    @classmethod
    def getMongoDBName(cls) -> str:
        """
        Returns the main DB name in string format.
        """
        return os.environ[EnvironmentVariablesTypes.MONGODB_DB_NAME.value]

    @classmethod
    def getWebserverPort(cls) -> int:
        """
        Returns the web server port in integer format.
        """
        return int(os.environ[EnvironmentVariablesTypes.WEBSERVER_PORT.value])

    @classmethod
    def getMasterKey(cls) -> str:
        """
        Returns the master key in string format.
        """
        return os.environ[EnvironmentVariablesTypes.MASTER_KEY.value]
