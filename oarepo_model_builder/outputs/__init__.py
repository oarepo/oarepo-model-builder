from pathlib import Path


class OutputBase:
    output_type = None

    def __init__(self, builder, path: Path):
        self.builder = builder
        self.path: Path = path
        self.executable = False

    def begin(self):
        raise NotImplementedError()

    def finish(self):
        raise NotImplementedError()

    @property
    def created(self):
        raise NotImplementedError()

    def make_executable(self):
        self.executable = True
