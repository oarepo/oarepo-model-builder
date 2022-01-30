from pathlib import Path


class AbstractFileSystem:
    def open(self, path, *args, **kwargs):
        raise Exception("Not implemented")

    def exists(self, path):
        raise Exception("Not implemented")

    def mkdir(self, path):
        raise Exception("Not implemented")

    def make_executable(self, path):
        pass


class FileSystem(AbstractFileSystem):
    def open(self, path, *args, **kwargs):
        return open(path, *args, **kwargs)

    def exists(self, path):
        return Path(path).exists()

    def mkdir(self, path):
        Path(path).mkdir(exist_ok=True, parents=True)

    def make_executable(self, path):
        Path(path).chmod(0o777)
