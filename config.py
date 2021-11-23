import configparser
from pathlib import Path


class Config:
    def __init__(self, configPath: Path) -> None:
        self.__config = configparser.ConfigParser()
        self.__config.read(configPath.absolute().__str__())

    def get(self, section: str, option: str) -> str:
        return self.__config.get(section, option)
