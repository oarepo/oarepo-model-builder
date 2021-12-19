from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class ElasticsearchModelPreprocessor(ModelPreprocessor):
    TYPE = 'elasticsearch'

    def transform(self, schema, settings):
        deepmerge(
            settings,
            {
                'elasticsearch': {
                    'version': 'v7',
                    'keyword-ignore-above': 50,
                    'templates': {
                        'v7': {
                            'mappings': {
                                "properties": {
                                    # TODO: tohle by melo byt v invenio baliku, ne tady -
                                    #  i kvuli marshmallow, schematu a tak
                                    "id": {
                                        "type": "keyword"
                                    },
                                    "created": {
                                        "type": "date"
                                    },
                                    "updated": {
                                        "type": "date"
                                    },
                                    "$schema": {
                                        "type": "keyword"
                                    },
                                    "pid": {
                                        "type": "object",
                                        "properties": {
                                            "pk": {
                                                "type": "integer"
                                            },
                                            "pid_type": {
                                                "type": "keyword"
                                            },
                                            "status": {
                                                "type": "keyword"
                                            },
                                            "obj_type": {
                                                "type": "keyword"
                                            }
                                        }
                                    },
                                    "uuid": {
                                        "type": "keyword"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )
