from io import StringIO
from pathlib import Path
from typing import Dict


class AbstractFileSystem:
    def open(self, path, *args, **kwargs):
        raise NotImplementedError("Not implemented")

    def exists(self, path):
        raise NotImplementedError("Not implemented")

    def mkdir(self, path):
        raise NotImplementedError("Not implemented")

    def make_executable(self, path):
        pass


class FileSystem(AbstractFileSystem):
    def __init__(self):
        self.opened_files = set()
        self.overwrite = False

    def open(self, path, mode="r", **kwargs):
        if self.overwrite:
            if "r" in mode and path not in self.opened_files:
                raise FileNotFoundError(f"File {path} not found")
            if "w" or "a" in mode:
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


class InMemoryFileSystem(AbstractFileSystem):
    def __init__(self):
        self.files: Dict[str, StringIO] = {}

    def open(self, path: str, mode: str = "r"):
        path = Path(path).absolute()
        if mode == "r":
            if not path in self.files:
                raise FileNotFoundError(
                    f"File {path} not found. Known files {[f for f in self.files]}"
                )
            return StringIO(self.files[path].getvalue())
        self.files[path] = StringIO()
        self.files[path].close = lambda: None
        return self.files[path]

    def exists(self, path):
        path = Path(path).absolute()
        return path in self.files

    def mkdir(self, path):
        pass

    def read(self, path):
        with self.open(path) as f:
            return f.read()

    def snapshot(self):
        ret = {}
        for fname, io in self.files.items():
            ret[fname] = io.getvalue()
        return ret
