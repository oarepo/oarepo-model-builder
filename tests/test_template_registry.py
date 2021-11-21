from oarepo_model_builder.templates import templates


def test_load_default_template():
    settings = {
        'invenio': {
            'templates': {}
        }
    }
    assert templates.get_template('record', settings)


def test_load_template_in_settings():
    settings = {
        'invenio': {
            'templates': {
                'blah': __file__
            }
        }
    }
    assert templates.get_template('blah', settings)
