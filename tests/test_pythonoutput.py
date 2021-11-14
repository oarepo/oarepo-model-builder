import tempfile
from pathlib import Path

from oarepo_model_builder.outputs.python import PythonOutput


def test_python():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py') as tmpf:
        tmpf.write("""
class Test:
    def __init__(self):
        pass
    @classmethod
    def a(self):
        # hola
        print(self)
    """)
        tmpf.flush()

        po = PythonOutput(Path(tmpf.name))
        po.begin()

        clz = po.get_class('Test1')

        po.finish()

        with open(tmpf.name) as f:
            content = f.read()
            print(content)
