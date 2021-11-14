from pathlib import Path


class OutputBase:
    output_type = None

    def __init__(self, path: Path):
        self.path: Path = path

    def begin(self):
        raise NotImplemented()

    def finish(self):
        raise NotImplemented()
