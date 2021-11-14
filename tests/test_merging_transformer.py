import libcst as cst

from oarepo_model_builder.utils.cst import MergingTransformer


def test_new_class():
    existing_module = "# comment start"
    included_module = """
# comment before
class Blah:
    # comment
    pass    
    """.strip()
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(included_module,
                                    config=original_cst.config_for_parsing)
    transformed_cst = original_cst.visit(MergingTransformer(included_cst))

    assert transformed_cst.code.strip() == """
# comment start
class Blah:
    # comment
    pass    
    """.strip()


def test_existing_class():
    existing_module = """
# comment start
class Blah:
    # comment
    pass    
    """.strip()
    included_module = existing_module

    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(included_module,
                                    config=original_cst.config_for_parsing)
    transformed_cst = original_cst.visit(MergingTransformer(included_cst))

    assert transformed_cst.code.strip() == existing_module.strip()


def test_new_function():
    existing_module = "# comment start"
    included_module = """
# comment before
def a():
    # comment
    return 1
        """.strip()
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(included_module,
                                    config=original_cst.config_for_parsing)
    transformed_cst = original_cst.visit(MergingTransformer(included_cst))

    assert transformed_cst.code.strip() == """
# comment start
def a():
    # comment
    return 1    
    """.strip()


def test_existing_function():
    existing_module = """
# comment start
def a():
    # comment
    return 1
        """.strip()
    included_module = """
def a():
    return 2
        """.strip()

    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(included_module,
                                    config=original_cst.config_for_parsing)
    transformed_cst = original_cst.visit(MergingTransformer(included_cst))

    assert transformed_cst.code.strip() == existing_module.strip()


def test_new_method():
    existing_module = """
# comment start
class Blah:
    # comment before
    def b(self):
        return 2
        """.strip()
    included_module = """
class Blah:
    # comment 2 before
    def a(self):
        return 1
        """.strip()

    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(included_module,
                                    config=original_cst.config_for_parsing)
    transformed_cst = original_cst.visit(MergingTransformer(included_cst))

    assert transformed_cst.code.strip() == """
# comment start
class Blah:
    # comment before
    def b(self):
        return 2
    # comment 2 before
    def a(self):
        return 1 
    """.strip()

def test_existing_method():
    existing_module = """
# comment start
class Blah:
    # comment before
    def b(self):
        return 2
        """.strip()
    included_module = """
class Blah:
    # comment 2 before
    def b(self):
        return 1
        """.strip()

    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(included_module,
                                    config=original_cst.config_for_parsing)
    transformed_cst = original_cst.visit(MergingTransformer(included_cst))

    assert transformed_cst.code.strip() == """
# comment start
class Blah:
    # comment before
    def b(self):
        return 2
    """.strip()


def test_new_include():
    existing_module = "# comment start"
    included_module = """
# comment before
import pathlib
from pathlib import (
    Blah
)
# comment after
class Blah:
    pass
        """.strip()
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(included_module,
                                    config=original_cst.config_for_parsing)
    transformed_cst = original_cst.visit(MergingTransformer(included_cst))

    assert transformed_cst.code.strip() == """
# comment start
import pathlib
from pathlib import (
    Blah
)
# comment after
class Blah:
    pass
        """.strip()


def test_existing_include():
    existing_module = """
# comment start
from c import d
import b
""".strip()
    included_module = """
# comment before
import b
import pathlib
from pathlib import (
    Blah
)
from c import d
from c import d, e
            """.strip()
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(included_module,
                                    config=original_cst.config_for_parsing)
    transformed_cst = original_cst.visit(MergingTransformer(included_cst))

    assert transformed_cst.code.strip() == """
# comment start
import pathlib
from pathlib import (
    Blah
)
from c import d, e
from c import d
import b
            """.strip()
