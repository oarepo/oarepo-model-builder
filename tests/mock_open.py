from io import StringIO
from pathlib import Path
from typing import Dict


class MockOpen:

    def __init__(self):
        self.files: Dict[str, StringIO] = {}

    def __call__(self, fname, mode='r'):
        fname = Path(fname).absolute()
        if mode == 'r':
            if not fname in self.files:
                raise FileNotFoundError(f'File {fname} not found. Known files {[f for f in self.files]}')
            return StringIO(self.files[fname].getvalue())
        self.files[fname] = StringIO()
        self.files[fname].close = lambda: None
        return self.files[fname]
