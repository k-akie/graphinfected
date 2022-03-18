import os


class FilePath:
    @staticmethod
    def __root() -> str:
        return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    @staticmethod
    def input(path: str = '') -> str:
        return os.path.join(FilePath.__root(), 'input', path)

    @staticmethod
    def output(path: str = '') -> str:
        return os.path.join(FilePath.__root(), 'output', path)

    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)
