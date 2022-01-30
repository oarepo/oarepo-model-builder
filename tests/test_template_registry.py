from oarepo_model_builder.templates import templates
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch


def test_load_default_template():
    settings = {
        "python": {
            "templates": {},
        }
    }
    assert templates.get_template("record", HyphenMunch(settings))


def test_load_template_in_settings():
    settings = {"python": {"templates": {"blah": __file__}}}
    assert templates.get_template("blah", HyphenMunch(settings))
