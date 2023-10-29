import pytest

from oarepo_model_builder.utils.python_name import Import, PythonQualifiedName


def test_python_qn():
    pn = PythonQualifiedName("C")
    assert pn.qualified_name == "C"
    assert pn.local_name == "C"
    assert pn.imports == []

    pn = PythonQualifiedName("a.b.C")
    assert pn.qualified_name == "a.b.C"
    assert pn.local_name == "C"
    assert pn.imports == [Import(import_path="a.b.C", alias=None)]

    pn = PythonQualifiedName("a.b.C{D}")
    assert pn.qualified_name == "a.b.C"
    assert pn.local_name == "D"
    assert pn.imports == [Import(import_path="a.b.C", alias="D")]

    pn = PythonQualifiedName("a.b{b.D}")
    assert pn.qualified_name == "a.b"
    assert pn.local_name == "b.D"
    assert pn.imports == [Import(import_path="a.b", alias="b")]

    with pytest.raises(ValueError):
        PythonQualifiedName("12.t")
