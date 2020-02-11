from configparser import ConfigParser, SectionProxy


class ConfigFile:
    def __init__(self, path: str):
        self.__path = path

        fake_str = "[root]\n"

        with open(self.__path) as file:
            fake_str += file.read()

        self.__config = ConfigParser()
        self.__config.optionxform = str
        self.__config.read_string(fake_str)

        self.__root_config: SectionProxy = self.__config["root"]

    def __getitem__(self, key):
        return self.__root_config[key]

    def __setitem__(self, key, value):
        self.__root_config[key] = value

    def sync_to_file(self) -> None:
        with open(self.__path, "w") as file:
            for key, value in self.__root_config.items():
                file.write(f"{key}={value}\n")
