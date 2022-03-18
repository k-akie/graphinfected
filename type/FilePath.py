import os


class FilePath:
    @staticmethod
    def __src() -> str:
        return os.path.dirname(os.path.dirname(__file__))

    @staticmethod
    def input(path: str = '') -> str:
        return os.path.join(FilePath.__src(), 'input', path)

    @staticmethod
    def output(path: str = '') -> str:
        return os.path.join(FilePath.__src(), 'output', path)
