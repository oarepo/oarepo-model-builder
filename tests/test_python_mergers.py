import re

import libcst as cst

from oarepo_model_builder.utils.cst import PythonContext, merge


def test_new_class():
    existing_module = "# comment start"
    included_module = """
# comment before
class Blah:
    # comment
    pass    
    """.strip()
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
# comment start
class Blah:
    # comment
    pass    
    """.strip()
    )


def test_existing_class():
    existing_module = """
# comment start
class Blah:
    # comment
    pass    
    """.strip()
    included_module = existing_module

    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

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
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
# comment start
def a():
    # comment
    return 1    
    """.strip()
    )


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
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

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
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
# comment start
class Blah:
    # comment before
    def b(self):
        return 2
    # comment 2 before
    def a(self):
        return 1 
    """.strip()
    )


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
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
# comment start
class Blah:
    # comment before
    def b(self):
        return 2
    """.strip()
    )


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
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
# comment start
import pathlib
from pathlib import (
    Blah
)
# comment after
class Blah:
    pass
        """.strip()
    )


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
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
# comment start
from c import d
import b
import pathlib
from pathlib import (
    Blah
)
from c import d, e
            """.strip()
    )


def test_top_level_vars():
    existing_module = ""
    included_module = """
AAA = "123"
BBB = "456"
            """.strip()
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
AAA = "123"
BBB = "456"
            """.strip()
    )


def test_top_level_merged_vars():
    existing_module = "CCC='456'"
    included_module = """
AAA = "123"
BBB = "456"
            """.strip()
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
CCC='456'
AAA = "123"
BBB = "456"
            """.strip()
    )


def test_merge_top_level_arrays():
    existing_module = "CCC=[1,2,3]"
    included_module = """CCC=[4,5,6,1]"""
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip().replace(" ", "")
        == """
CCC=[1,2,3,4,5,6,]
            """.strip()
    )


def test_do_not_overwrite_top_level_vars():
    existing_module = "CCC=234"
    included_module = """CCC=438"""
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert (
        transformed_cst.code.strip()
        == """
CCC=234
            """.strip()
    )


def test_merge_class_arrays():
    existing_module = """
class A:
    CCC=[1,2,3]
    """
    included_module = """
class A:
    CCC=[4,5,6]
    """
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert re.sub(r"[\t\n ]", "", transformed_cst.code) == re.sub(
        r"[\t\n ]",
        "",
        """
class A:
CCC=[1,2,3,4,5,6]
            """,
    )


def test_merge_arguments():
    existing_module = """
a = blah(1, 2, 3)    
    """
    included_module = """
a = blah(1, 2, 4)   
"""
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert re.sub(r"[\t\n ]", "", transformed_cst.code) == re.sub(
        r"[\t\n ]", "", existing_module
    )


def test_merge_kwarguments():
    existing_module = """
a = blah(1, 2, b=3)    
    """
    included_module = """
a = blah(1, 2, d=4)   
"""
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert re.sub(r"[\t\n ]", "", transformed_cst.code) == re.sub(
        r"[\t\n ]",
        "",
        """
a = blah(1, 2, b=3, d=4)    
    """,
    )


def test_merge_argument_list():
    existing_module = """
a = blah(1, 2, [3])    
    """
    included_module = """
a = blah(1, 2, [4])   
"""
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert re.sub(r"[\t\n ]", "", transformed_cst.code) == re.sub(
        r"[\t\n ]",
        "",
        """
a = blah(1, 2, [3, 4])    
    """,
    )


def test_merge_kwargument_list():
    existing_module = """
a = blah(1, 2, b=[3])    
    """
    included_module = """
a = blah(1, 2, b=[4])   
"""
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert re.sub(r"[\t\n ]", "", transformed_cst.code) == re.sub(
        r"[\t\n ]",
        "",
        """
a = blah(1, 2, b=[3, 4])    
    """,
    )


def test_dict_merge():
    existing_module = """
a = {'a': 1, 'b': 2}  
        """
    included_module = """
a = {'c': 3}
    """
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert re.sub(r"[\t\n ]", "", transformed_cst.code) == re.sub(
        r"[\t\n ]",
        "",
        """
    a = {'a': 1, 'b': 2, 'c': 3}
        """,
    )


def test_dict_merge_overwrite():
    existing_module = """
a = {'a': 1}  
            """
    included_module = """
a = {'a': 2}
        """
    original_cst = cst.parse_module(existing_module)
    included_cst = cst.parse_module(
        included_module, config=original_cst.config_for_parsing
    )
    transformed_cst = merge(PythonContext(included_cst), original_cst, included_cst)

    assert re.sub(r"[\t\n ]", "", transformed_cst.code) == re.sub(
        r"[\t\n ]",
        "",
        """
        a = {'a': 1}
            """,
    )
