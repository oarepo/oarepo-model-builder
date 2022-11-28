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
    def __init__(self):
        self.opened_files = set()
        self.overwrite = False

    def open(self, path, mode='r', **kwargs):
        if self.overwrite:
            if 'r' in mode and path not in self.opened_files:
                raise FileNotFoundError(f"File {path} not found")
            if 'w' or 'a' in mode:
                self.opened_files.add(path)
        return open(path, mode=mode, **kwargs)

    def exists(self, path):
        # if overwrite and the file has not been saved, return False
        if self.overwrite:
            return path in self.opened_files
        return Path(path).exists()

    def mkdir(self, path):
        Path(path).mkdir(exist_ok=True, parents=True)

    def make_executable(self, path):
        Path(path).chmod(0o777)
