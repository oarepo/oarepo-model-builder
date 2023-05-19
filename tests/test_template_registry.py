from oarepo_model_builder.templates import templates


def test_load_default_template():
    settings = {
        "python": {
            "templates": {},
        }
    }
    assert templates.get_template("record", settings)
