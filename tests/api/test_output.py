from oarepo_model_builder.outputs.output import BaseOutput, MappingOutput, JsonSchemaOutput


def test_base_output():
    bo = BaseOutput('', {'test': 'data'})

    assert bo.path == ''
    assert bo.output_type == None
    assert bo.data == {'test': 'data'}

    bo.set(['testpath', 'subpath', 'subsub'], 'test1')
    bo.set(['testpath', 'subpath', 'subsub2'], 'test2')

    assert bo.data == {
        'test': 'data',
        'testpath': {
            'subpath': {
                'subsub': 'test1',
                'subsub2': 'test2'
            }
        }
    }


def test_mapping_output(app):
    mo = MappingOutput(path='')

    assert mo.output_type == 'mapping'
    assert mo.path == ''
    assert mo.data == {
        "settings": {
            "analysis": {
                "char_filter": {
                    "configured_html_strip": {
                        "type": "html_strip",
                        "escaped_tags": []
                    }
                },
                "normalizer": {
                    "wsnormalizer": {
                        "type": "custom",
                        "filter": [
                            "trim"
                        ]
                    }
                },
                "filter": {
                    "czech_stop": {
                        "type": "stop",
                        "stopwords": "_czech_"
                    },
                    "czech_stemmer": {
                        "type": "stemmer",
                        "language": "czech"
                    }
                },
                "analyzer": {
                    "default": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "czech_stop",
                            "czech_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "dynamic": False,
            "date_detection": False,
            "numeric_detection": False,
            "properties": {}
        }
    }


def test_jsonschema_output(app):
    jo = JsonSchemaOutput(path='')

    assert jo.output_type == 'jsonschema'
    assert jo.path == ''
    assert jo.data == {
        "type": "object",
        "additionalProperties": False
    }
