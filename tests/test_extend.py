from pathlib import Path
from typing import Union

import json5

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem
from oarepo_model_builder.profiles import Profile
from oarepo_model_builder.profiles.extend import ExtendProfile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.schema import ModelSchema


def check_marshmallow(x, path):
    if isinstance(x, (list, tuple)):
        for i, xx in enumerate(x):
            check_marshmallow(xx, f"{path}.{i}")
    elif isinstance(x, dict):
        if "marshmallow" in x:
            m = x["marshmallow"]
            if "schema-class" in m and m.get("generate") is not False:
                raise AssertionError(
                    f"Error on path {path}: marshmallow gets generated"
                )
        for k, v in x.items():
            check_marshmallow(v, f"{path}.{k}")


def test_extend_property_preprocessor():
    fs = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(
        profile="extend",
        filesystem=fs,
    )

    model = ModelSchema(
        "/tmp/test.json", content=nr_documents_model  # NOSONAR
    )  # NOSONAR - this is fake path on memory filesystem
    ExtendProfile().build(model, "", builder, disable_validation=True)
    loaded_model = json5.loads(fs.read("model.json5"))
    # assert that no class is generated in loaded_model
    check_marshmallow(loaded_model, "")


nr_documents_model = {
    "model": {
        "type": "object",
        "cli-function": "nr_metadata.documents.cli.group",
        "properties": {
            "metadata": {
                "marshmallow": {
                    "base-classes": ["ma.Schema"],
                    "field-class": "ma_fields.Nested",  # NOSONAR
                    "schema-class": "nr_metadata.documents.services.records.schema.NRDocumentMetadataSchema",
                    "imports": [
                        {
                            "import": "nr_metadata.documents.services.records.schema.NRDocumentMetadataSchema"
                        }
                    ],
                    "generate": True,
                    "validators": [],
                },
                "properties": {
                    "thesis": {
                        "marshmallow": {
                            "field-class": "ma_fields.Nested",
                            "schema-class": "nr_metadata.documents.services.records.schema.NRThesisSchema",
                            "imports": [
                                {
                                    "import": "nr_metadata.documents.services.records.schema.NRThesisSchema"
                                }
                            ],
                            "validators": [],
                        },
                        "properties": {
                            "dateDefended": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",  # NOSONAR
                                    "validators": ["validate_date('%Y-%m-%d')"],
                                    "imports": [
                                        {
                                            "import": "oarepo_runtime.validation.validate_date"
                                        },
                                        {
                                            "import": "oarepo_runtime.ui.marshmallow",  # NOSONAR
                                            "alias": "l10n",
                                        },
                                        {
                                            "import": "oarepo_runtime.validation.validate_date"
                                        },
                                        {
                                            "import": "oarepo_runtime.ui.marshmallow",
                                            "alias": "l10n",
                                        },
                                    ],
                                },
                                "label.cs": "Datum obhajoby",  # NOSONAR
                                "ui": {
                                    "marshmallow": {"field-class": "l10n.LocalizedDate"}
                                },
                                "label.en": "Date defended",  # NOSONAR
                                "type": "date",
                            },
                            "defended": {
                                "marshmallow": {
                                    "field-class": "ma_fields.Boolean",
                                    "validators": [],
                                    "imports": [],
                                },
                                "label.cs": "Obhájeno?",
                                "ui": {
                                    "marshmallow": {"field-class": "ma_fields.Boolean"}
                                },
                                "label.en": "Defended?",
                                "type": "boolean",
                            },
                            "degreeGrantors": {
                                "marshmallow": {
                                    "field-class": "ma_fields.List",  # NOSONAR
                                    "validators": [],
                                    "imports": [],
                                },
                                "label.cs": "Instituce / grantor",
                                "items": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.documents.services.records.schema.NRDegreeGrantorSchema",
                                        "imports": [
                                            {
                                                "import": "nr_metadata.documents.services.records.schema.NRDegreeGrantorSchema"
                                            }
                                        ],
                                        "validators": [],
                                    },
                                    "properties": {
                                        "id": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "sample": {"skip": True},
                                            "type": "keyword",
                                            "mapping": {
                                                "fields": {
                                                    "text": {
                                                        "type": "search_as_you_type"
                                                    }
                                                }
                                            },
                                        },
                                        "title": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",  # NOSONAR
                                                "imports": [
                                                    {
                                                        "import": "invenio_vocabularies.services.schema.i18n_strings"  # NOSONAR
                                                    }
                                                ],
                                                "validators": [],
                                                "field": "i18n_strings",
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",  # NOSONAR
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"  # NOSONAR
                                                        }
                                                    ],
                                                    "generate": False,
                                                    "field": "VocabularyI18nStrUIField()",  # NOSONAR
                                                }
                                            },
                                            "additionalProperties": {"type": "string"},
                                            "propertyNames": {"pattern": "^[a-z]{2}$"},
                                            "type": "object",
                                            "mapping": {
                                                "properties": {
                                                    "en": {"type": "search_as_you_type"}
                                                },
                                                "dynamic": True,
                                            },
                                        },
                                        "type": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                        "hierarchy": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",  # NOSONAR
                                                "imports": [
                                                    {
                                                        "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                    }
                                                ],
                                                "generate": False,
                                                "validators": [],
                                            },
                                            "properties": {
                                                "parent": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "validators": [],
                                                        "imports": [],
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String"
                                                        }
                                                    },
                                                    "type": "keyword",
                                                },
                                                "level": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Integer",  # NOSONAR
                                                        "validators": [],
                                                        "imports": [],
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Integer"
                                                        }
                                                    },
                                                    "type": "integer",
                                                },
                                                "title": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.List",
                                                        "validators": [],
                                                        "imports": [],
                                                    },
                                                    "items": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Nested",
                                                            "schema-class": "nr_metadata.documents.services.records.schema.TitleItemSchema",  # NOSONAR
                                                            "validators": [],
                                                            "field": "i18n_strings",
                                                            "imports": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Nested",
                                                                "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleItemUISchema",  # NOSONAR
                                                                "field": "i18n_strings",
                                                            }
                                                        },
                                                        "additionalProperties": {
                                                            "type": "string"
                                                        },
                                                        "propertyNames": {
                                                            "pattern": "^[a-z]{2}$"
                                                        },
                                                        "type": "object",
                                                        "mapping": {"dynamic": True},
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.List"
                                                        }
                                                    },
                                                    "type": "array",
                                                },
                                                "ancestors": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.List",
                                                        "validators": [],
                                                        "imports": [],
                                                    },
                                                    "items": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String"
                                                            }
                                                        },
                                                        "type": "keyword",
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.List"
                                                        }
                                                    },
                                                    "type": "array",
                                                },
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",  # NOSONAR
                                                    "generate": False,
                                                }
                                            },
                                            "type": "object",
                                        },
                                        "@v": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "validators": [],
                                                "field-name": "_version",
                                                "imports": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "field-name": "_version",
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                    },
                                    "ui": {
                                        "detail": "nr_degree_grantor",
                                        "edit": "taxonomy_item",
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.documents.services.records.ui_schema.NRDegreeGrantorUISchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.documents.services.records.ui_schema.NRDegreeGrantorUISchema"
                                                }
                                            ],
                                        },
                                    },
                                    "pid-field": 'Vocabulary.pid.with_type_ctx("institutions")',  # NOSONAR
                                    "imports": [
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"  # NOSONAR
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.RelationsField"  # NOSONAR
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.PIDRelation"  # NOSONAR
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.InternalRelation"  # NOSONAR
                                        },
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                    ],
                                    "model": "vocabularies",
                                    "schema-prefix": "DegreegrantorsItem",
                                    "name": "degreeGrantors_item",
                                    "relation-class": "PIDRelation",
                                    "keys": [
                                        {"target": "id", "key": "id"},
                                        {"target": "title", "key": "title"},
                                        {"target": "type", "key": "type.id"},
                                        {
                                            "model": {
                                                "properties": {
                                                    "parent": {"type": "keyword"},
                                                    "level": {"type": "integer"},
                                                    "title": {
                                                        "items": {
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field": "i18n_strings"
                                                                }
                                                            },
                                                            "marshmallow": {
                                                                "field": "i18n_strings"
                                                            },
                                                            "additionalProperties": {
                                                                "type": "string"
                                                            },
                                                            "propertyNames": {
                                                                "pattern": "^[a-z]{2}$"
                                                            },
                                                            "type": "object",
                                                            "mapping": {
                                                                "dynamic": True
                                                            },
                                                        },
                                                        "type": "array",
                                                    },
                                                    "ancestors": {
                                                        "items": {"type": "keyword"},
                                                        "type": "array",
                                                    },
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                        "generate": False,
                                                    }
                                                },
                                                "marshmallow": {
                                                    "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                        }
                                                    ],
                                                    "generate": False,
                                                },
                                                "type": "object",
                                            },
                                            "target": "hierarchy",
                                            "key": "hierarchy",
                                        },
                                    ],
                                    "model-class": "Vocabulary",
                                    "relation-args": {
                                        "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}, 'hierarchy']",  # NOSONAR
                                        "pid_field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                    },
                                    "type": "relation",
                                },
                                "ui": {
                                    "marshmallow": {"field-class": "ma_fields.List"}
                                },
                                "label.en": "Degree grantor",
                                "type": "array",
                            },
                            "studyFields": {
                                "marshmallow": {
                                    "field-class": "ma_fields.List",
                                    "validators": [],
                                    "imports": [],
                                },
                                "label.cs": "Oblasti studia",
                                "items": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "keyword",
                                },
                                "ui": {
                                    "marshmallow": {"field-class": "ma_fields.List"}
                                },
                                "label.en": "Study fields",
                                "type": "array",
                            },
                        },
                        "ui": {
                            "detail": "thesis",
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.documents.services.records.ui_schema.NRThesisUISchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.documents.services.records.ui_schema.NRThesisUISchema"
                                    }
                                ],
                            },
                        },
                        "type": "object",
                    },
                    "collection": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Kolekce",
                        "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                        "label.en": "Collection",
                        "type": "keyword",
                    },
                    "title": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Název",
                        "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                        "label.en": "Title",
                        "type": "fulltext+keyword",  # NOSONAR
                        "required": True,
                    },
                    "additionalTitles": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Další názvy",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.AdditionalTitlesSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.AdditionalTitlesSchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "properties": {
                                "title": {
                                    "marshmallow": {
                                        "field-class": "I18nStrField",
                                        "schema-class": None,
                                        "imports": [
                                            {
                                                "import": "oarepo_runtime.i18n.schema.I18nStrField"  # NOSONAR
                                            }
                                        ],
                                        "generate": False,
                                        "validators": [],
                                    },
                                    "properties": {
                                        "lang": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "validators": [],
                                                "imports": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String"
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                        "value": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "validators": [],
                                                "imports": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String"
                                                }
                                            },
                                            "type": "fulltext+keyword",
                                        },
                                    },
                                    "ui": {
                                        "detail": "multilingual",
                                        "marshmallow": {
                                            "field-class": "I18nStrUIField",
                                            "schema-class": None,
                                            "imports": [
                                                {
                                                    "import": "oarepo_runtime.i18n.ui_schema.I18nStrUIField"  # NOSONAR
                                                }
                                            ],
                                        },
                                    },
                                    "sample": {"skip": False},
                                    "type": "i18nStr",
                                    "required": True,
                                },
                                "titleType": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                        ],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "l10n.LocalizedEnum",  # NOSONAR
                                            "arguments": [
                                                'value_prefix="nr_metadata.documents"'  # NOSONAR
                                            ],
                                        }
                                    },
                                    "enum": [
                                        "translatedTitle",
                                        "alternativeTitle",
                                        "subtitle",
                                        "other",
                                    ],
                                    "type": "keyword",
                                    "required": True,
                                },
                            },
                            "ui": {
                                "detail": "additionalTitle",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.AdditionalTitlesUISchema",
                                },
                            },
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Additional titles",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "creators": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Autoři",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRAuthoritySchema",  # NOSONAR
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRAuthoritySchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "properties": {
                                "affiliations": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.List",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.schema.NRAffiliationVocabularySchema",  # NOSONAR
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.schema.NRAffiliationVocabularySchema"
                                                }
                                            ],
                                            "validators": [],
                                        },
                                        "label.cs": "Afiliace",
                                        "properties": {
                                            "id": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "imports": [],
                                                        "validators": [],
                                                    }
                                                },
                                                "sample": {"skip": True},
                                                "type": "keyword",
                                                "mapping": {
                                                    "fields": {
                                                        "text": {
                                                            "type": "search_as_you_type"
                                                        }
                                                    }
                                                },
                                            },
                                            "title": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                    "imports": [
                                                        {
                                                            "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                        }
                                                    ],
                                                    "validators": [],
                                                    "field": "i18n_strings",
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                        "imports": [
                                                            {
                                                                "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                            }
                                                        ],
                                                        "generate": False,
                                                        "field": "VocabularyI18nStrUIField()",
                                                    }
                                                },
                                                "additionalProperties": {
                                                    "type": "string"
                                                },
                                                "propertyNames": {
                                                    "pattern": "^[a-z]{2}$"
                                                },
                                                "type": "object",
                                                "mapping": {
                                                    "properties": {
                                                        "en": {
                                                            "type": "search_as_you_type"
                                                        }
                                                    },
                                                    "dynamic": True,
                                                },
                                            },
                                            "type": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "imports": [],
                                                        "validators": [],
                                                    }
                                                },
                                                "type": "keyword",
                                            },
                                            "hierarchy": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                        }
                                                    ],
                                                    "generate": False,
                                                    "validators": [],
                                                },
                                                "properties": {
                                                    "parent": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String"
                                                            }
                                                        },
                                                        "type": "keyword",
                                                    },
                                                    "level": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Integer",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Integer"
                                                            }
                                                        },
                                                        "type": "integer",
                                                    },
                                                    "title": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.List",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "items": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Nested",
                                                                "schema-class": "nr_metadata.documents.services.records.schema.TitleItemSchema",
                                                                "validators": [],
                                                                "field": "i18n_strings",
                                                                "imports": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.Nested",
                                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleItemUISchema",
                                                                    "field": "i18n_strings",
                                                                }
                                                            },
                                                            "additionalProperties": {
                                                                "type": "string"
                                                            },
                                                            "propertyNames": {
                                                                "pattern": "^[a-z]{2}$"
                                                            },
                                                            "type": "object",
                                                            "mapping": {
                                                                "dynamic": True
                                                            },
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.List"
                                                            }
                                                        },
                                                        "type": "array",
                                                    },
                                                    "ancestors": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.List",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "items": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "validators": [],
                                                                "imports": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String"
                                                                }
                                                            },
                                                            "type": "keyword",
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.List"
                                                            }
                                                        },
                                                        "type": "array",
                                                    },
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                        "generate": False,
                                                    }
                                                },
                                                "type": "object",
                                            },
                                            "@v": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "field-name": "_version",
                                                    "imports": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "field-name": "_version",
                                                    }
                                                },
                                                "type": "keyword",
                                            },
                                        },
                                        "ui": {
                                            "detail": "taxonomy_item",
                                            "edit": "taxonomy_item",
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "nr_metadata.common.services.records.ui_schema.NRAffiliationVocabularyUISchema",  # NOSONAR
                                                "imports": [
                                                    {
                                                        "import": "nr_metadata.common.services.records.ui_schema.NRAffiliationVocabularyUISchema"
                                                    }
                                                ],
                                            },
                                        },
                                        "pid-field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                        "label.en": "Affiliation",
                                        "sample": {"skip": False, "faker": "company"},
                                        "imports": [
                                            {
                                                "import": "invenio_vocabularies.records.api.Vocabulary"
                                            },
                                            {
                                                "import": "oarepo_runtime.relations.RelationsField"
                                            },
                                            {
                                                "import": "oarepo_runtime.relations.PIDRelation"
                                            },
                                            {
                                                "import": "oarepo_runtime.relations.InternalRelation"
                                            },
                                            {
                                                "import": "invenio_vocabularies.records.api.Vocabulary"
                                            },
                                        ],
                                        "model": "vocabularies",
                                        "hint.cs": "Uveďte instituci/instituce, pod jejíž záštitou jste se na tvorbě objektu podíleli.",  # NOSONAR
                                        "schema-prefix": "AffiliationsItem",
                                        "name": "affiliations_item",
                                        "relation-class": "PIDRelation",
                                        "keys": [
                                            {"target": "id", "key": "id"},
                                            {"target": "title", "key": "title"},
                                            {"target": "type", "key": "type.id"},
                                            {
                                                "model": {
                                                    "properties": {
                                                        "parent": {"type": "keyword"},
                                                        "level": {"type": "integer"},
                                                        "title": {
                                                            "items": {
                                                                "ui": {
                                                                    "marshmallow": {
                                                                        "field": "i18n_strings"
                                                                    }
                                                                },
                                                                "marshmallow": {
                                                                    "field": "i18n_strings"
                                                                },
                                                                "additionalProperties": {
                                                                    "type": "string"
                                                                },
                                                                "propertyNames": {
                                                                    "pattern": "^[a-z]{2}$"
                                                                },
                                                                "type": "object",
                                                                "mapping": {
                                                                    "dynamic": True
                                                                },
                                                            },
                                                            "type": "array",
                                                        },
                                                        "ancestors": {
                                                            "items": {
                                                                "type": "keyword"
                                                            },
                                                            "type": "array",
                                                        },
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                            "generate": False,
                                                        }
                                                    },
                                                    "marshmallow": {
                                                        "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                        "imports": [
                                                            {
                                                                "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                            }
                                                        ],
                                                        "generate": False,
                                                    },
                                                    "type": "object",
                                                },
                                                "target": "hierarchy",
                                                "key": "hierarchy",
                                            },
                                        ],
                                        "model-class": "Vocabulary",
                                        "relation-args": {
                                            "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}, 'hierarchy']",
                                            "pid_field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                        },
                                        "type": "relation",
                                    },
                                    "ui": {
                                        "marshmallow": {"field-class": "ma_fields.List"}
                                    },
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                                "nameType": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                        ],
                                    },
                                    "label.cs": "Typ",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "l10n.LocalizedEnum",
                                            "arguments": [
                                                'value_prefix="nr_metadata.documents"'
                                            ],
                                        }
                                    },
                                    "label.en": "Type",
                                    "sample": [True, True],
                                    "hint.cs": "Jako tvůrce je možné označit osobu nebo instituci.",  # NOSONAR
                                    "enum": ["Organizational", "Personal"],
                                    "hint.en": "It is possible to designate a person or an institution as the creator/contributor.",  # NOSONAR
                                    "type": "keyword",
                                },
                                "fullName": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "sample": {"skip": False, "faker": "name"},
                                    "type": "keyword",
                                    "required": True,
                                },
                                "authorityIdentifiers": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.List",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema",  # NOSONAR
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema"
                                                }
                                            ],
                                            "generate": False,
                                            "validators": [],
                                        },
                                        "properties": {
                                            "identifier": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "label.cs": "Identifikátor",  # NOSONAR
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String"
                                                    }
                                                },
                                                "label.en": "Identifier",
                                                "sample": {
                                                    "skip": False,
                                                    "faker": "isbn13",
                                                },
                                                "i18n.key": "identifier",  # NOSONAR
                                                "type": "keyword",
                                                "required": True,
                                            },
                                            "scheme": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                    ],
                                                },
                                                "label.cs": "Typ identifikátoru",  # NOSONAR
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "l10n.LocalizedEnum",
                                                        "arguments": [
                                                            'value_prefix="nr_metadata.documents"'
                                                        ],
                                                    }
                                                },
                                                "label.en": "Identifier type",  # NOSONAR
                                                "hint.cs": "Doporučujeme zadat alespoň jeden z typů identifikátorů.\nPokud potřebujete rozšířit nabídku typů identifikátorů, kontaktujte nás na support@narodni-repozitar.cz.\n",  # NOSONAR
                                                "enum": [
                                                    "orcid",
                                                    "scopusID",
                                                    "researcherID",
                                                    "czenasAutID",
                                                    "vedidk",
                                                    "institutionalID",
                                                    "ISNI",
                                                    "ROR",
                                                    "ICO",
                                                    "DOI",
                                                ],
                                                "hint.en": "We recommend providing at least one of the identifier types.\nIf you need to expand the range of identifier types, contact us at support@narodni-repozitar.cz.\n",  # NOSONAR
                                                "i18n.key": "identifier_type",
                                                "type": "keyword",
                                                "required": True,
                                            },
                                        },
                                        "ui": {
                                            "detail": "nr_authority_identifier",
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema",  # NOSONAR
                                                "imports": [
                                                    {
                                                        "import": "nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema"
                                                    }
                                                ],
                                                "generate": False,
                                            },
                                        },
                                        "type": "object",
                                    },
                                    "ui": {
                                        "marshmallow": {"field-class": "ma_fields.List"}
                                    },
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            },
                            "ui": {
                                "detail": "creator",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRAuthorityUIUISchema",  # NOSONAR
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRAuthorityUIUISchema"
                                        }
                                    ],
                                },
                            },
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Authors",
                        "uniqueItems": True,
                        "minItems": 1,
                        "type": "array",
                        "required": True,
                    },
                    "contributors": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Přispěvatelé",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRContributorSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRContributorSchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "properties": {
                                "role": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.common.services.records.schema.NRAuthorityRoleVocabularySchema",  # NOSONAR
                                        "imports": [
                                            {
                                                "import": "nr_metadata.common.services.records.schema.NRAuthorityRoleVocabularySchema"
                                            }
                                        ],
                                        "validators": [],
                                    },
                                    "label.cs": "Role přispěvatele",
                                    "properties": {
                                        "id": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "sample": {"skip": True},
                                            "type": "keyword",
                                            "mapping": {
                                                "fields": {
                                                    "text": {
                                                        "type": "search_as_you_type"
                                                    }
                                                }
                                            },
                                        },
                                        "title": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                "imports": [
                                                    {
                                                        "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                    }
                                                ],
                                                "validators": [],
                                                "field": "i18n_strings",
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                        }
                                                    ],
                                                    "generate": False,
                                                    "field": "VocabularyI18nStrUIField()",
                                                }
                                            },
                                            "additionalProperties": {"type": "string"},
                                            "propertyNames": {"pattern": "^[a-z]{2}$"},
                                            "type": "object",
                                            "mapping": {
                                                "properties": {
                                                    "en": {"type": "search_as_you_type"}
                                                },
                                                "dynamic": True,
                                            },
                                        },
                                        "type": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                        "@v": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "validators": [],
                                                "field-name": "_version",
                                                "imports": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "field-name": "_version",
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                    },
                                    "ui": {
                                        "detail": "vocabulary_item",
                                        "edit": "vocabulary_item",
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.ui_schema.NRAuthorityRoleVocabularyUISchema",  # NOSONAR
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.ui_schema.NRAuthorityRoleVocabularyUISchema"
                                                }
                                            ],
                                        },
                                    },
                                    "pid-field": 'Vocabulary.pid.with_type_ctx("contributor-roles")',  # NOSONAR
                                    "label.en": "Contributor's role",
                                    "imports": [
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.RelationsField"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.PIDRelation"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.InternalRelation"
                                        },
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                    ],
                                    "model": "vocabularies",
                                    "schema-prefix": "Role",
                                    "name": "role",
                                    "relation-class": "PIDRelation",
                                    "keys": [
                                        {"target": "id", "key": "id"},
                                        {"target": "title", "key": "title"},
                                        {"target": "type", "key": "type.id"},
                                    ],
                                    "model-class": "Vocabulary",
                                    "relation-args": {
                                        "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",  # NOSONAR
                                        "pid_field": 'Vocabulary.pid.with_type_ctx("contributor-roles")',
                                    },
                                    "type": "relation",
                                },
                                "affiliations": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.List",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.schema.NRAffiliationVocabularySchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.schema.NRAffiliationVocabularySchema"
                                                }
                                            ],
                                            "validators": [],
                                        },
                                        "label.cs": "Afiliace",
                                        "properties": {
                                            "id": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "imports": [],
                                                        "validators": [],
                                                    }
                                                },
                                                "sample": {"skip": True},
                                                "type": "keyword",
                                                "mapping": {
                                                    "fields": {
                                                        "text": {
                                                            "type": "search_as_you_type"
                                                        }
                                                    }
                                                },
                                            },
                                            "title": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                    "imports": [
                                                        {
                                                            "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                        }
                                                    ],
                                                    "validators": [],
                                                    "field": "i18n_strings",
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                        "imports": [
                                                            {
                                                                "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                            }
                                                        ],
                                                        "generate": False,
                                                        "field": "VocabularyI18nStrUIField()",
                                                    }
                                                },
                                                "additionalProperties": {
                                                    "type": "string"
                                                },
                                                "propertyNames": {
                                                    "pattern": "^[a-z]{2}$"
                                                },
                                                "type": "object",
                                                "mapping": {
                                                    "properties": {
                                                        "en": {
                                                            "type": "search_as_you_type"
                                                        }
                                                    },
                                                    "dynamic": True,
                                                },
                                            },
                                            "type": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "imports": [],
                                                        "validators": [],
                                                    }
                                                },
                                                "type": "keyword",
                                            },
                                            "hierarchy": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                        }
                                                    ],
                                                    "generate": False,
                                                    "validators": [],
                                                },
                                                "properties": {
                                                    "parent": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String"
                                                            }
                                                        },
                                                        "type": "keyword",
                                                    },
                                                    "level": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Integer",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Integer"
                                                            }
                                                        },
                                                        "type": "integer",
                                                    },
                                                    "title": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.List",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "items": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Nested",
                                                                "schema-class": "nr_metadata.documents.services.records.schema.TitleItemSchema",
                                                                "validators": [],
                                                                "field": "i18n_strings",
                                                                "imports": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.Nested",
                                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleItemUISchema",
                                                                    "field": "i18n_strings",
                                                                }
                                                            },
                                                            "additionalProperties": {
                                                                "type": "string"
                                                            },
                                                            "propertyNames": {
                                                                "pattern": "^[a-z]{2}$"
                                                            },
                                                            "type": "object",
                                                            "mapping": {
                                                                "dynamic": True
                                                            },
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.List"
                                                            }
                                                        },
                                                        "type": "array",
                                                    },
                                                    "ancestors": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.List",
                                                            "validators": [],
                                                            "imports": [],
                                                        },
                                                        "items": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "validators": [],
                                                                "imports": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String"
                                                                }
                                                            },
                                                            "type": "keyword",
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.List"
                                                            }
                                                        },
                                                        "type": "array",
                                                    },
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                        "generate": False,
                                                    }
                                                },
                                                "type": "object",
                                            },
                                            "@v": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "field-name": "_version",
                                                    "imports": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "field-name": "_version",
                                                    }
                                                },
                                                "type": "keyword",
                                            },
                                        },
                                        "ui": {
                                            "detail": "taxonomy_item",
                                            "edit": "taxonomy_item",
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "nr_metadata.common.services.records.ui_schema.NRAffiliationVocabularyUISchema",
                                                "imports": [
                                                    {
                                                        "import": "nr_metadata.common.services.records.ui_schema.NRAffiliationVocabularyUISchema"
                                                    }
                                                ],
                                            },
                                        },
                                        "pid-field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                        "label.en": "Affiliation",
                                        "sample": {"skip": False, "faker": "company"},
                                        "imports": [
                                            {
                                                "import": "invenio_vocabularies.records.api.Vocabulary"
                                            },
                                            {
                                                "import": "oarepo_runtime.relations.RelationsField"
                                            },
                                            {
                                                "import": "oarepo_runtime.relations.PIDRelation"
                                            },
                                            {
                                                "import": "oarepo_runtime.relations.InternalRelation"
                                            },
                                            {
                                                "import": "invenio_vocabularies.records.api.Vocabulary"
                                            },
                                        ],
                                        "model": "vocabularies",
                                        "hint.cs": "Uveďte instituci/instituce, pod jejíž záštitou jste se na tvorbě objektu podíleli.",
                                        "schema-prefix": "AffiliationsItem",
                                        "name": "affiliations_item",
                                        "relation-class": "PIDRelation",
                                        "keys": [
                                            {"target": "id", "key": "id"},
                                            {"target": "title", "key": "title"},
                                            {"target": "type", "key": "type.id"},
                                            {
                                                "model": {
                                                    "properties": {
                                                        "parent": {"type": "keyword"},
                                                        "level": {"type": "integer"},
                                                        "title": {
                                                            "items": {
                                                                "ui": {
                                                                    "marshmallow": {
                                                                        "field": "i18n_strings"
                                                                    }
                                                                },
                                                                "marshmallow": {
                                                                    "field": "i18n_strings"
                                                                },
                                                                "additionalProperties": {
                                                                    "type": "string"
                                                                },
                                                                "propertyNames": {
                                                                    "pattern": "^[a-z]{2}$"
                                                                },
                                                                "type": "object",
                                                                "mapping": {
                                                                    "dynamic": True
                                                                },
                                                            },
                                                            "type": "array",
                                                        },
                                                        "ancestors": {
                                                            "items": {
                                                                "type": "keyword"
                                                            },
                                                            "type": "array",
                                                        },
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                            "generate": False,
                                                        }
                                                    },
                                                    "marshmallow": {
                                                        "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                        "imports": [
                                                            {
                                                                "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                            }
                                                        ],
                                                        "generate": False,
                                                    },
                                                    "type": "object",
                                                },
                                                "target": "hierarchy",
                                                "key": "hierarchy",
                                            },
                                        ],
                                        "model-class": "Vocabulary",
                                        "relation-args": {
                                            "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}, 'hierarchy']",
                                            "pid_field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                        },
                                        "type": "relation",
                                    },
                                    "ui": {
                                        "marshmallow": {"field-class": "ma_fields.List"}
                                    },
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                                "nameType": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                        ],
                                    },
                                    "label.cs": "Typ",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "l10n.LocalizedEnum",
                                            "arguments": [
                                                'value_prefix="nr_metadata.documents"'
                                            ],
                                        }
                                    },
                                    "label.en": "Type",
                                    "sample": [True, True],
                                    "hint.cs": "Jako tvůrce je možné označit osobu nebo instituci.",
                                    "enum": ["Organizational", "Personal"],
                                    "hint.en": "It is possible to designate a person or an institution as the creator/contributor.",
                                    "type": "keyword",
                                },
                                "fullName": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "sample": {"skip": False, "faker": "name"},
                                    "type": "keyword",
                                    "required": True,
                                },
                                "authorityIdentifiers": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.List",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema"
                                                }
                                            ],
                                            "generate": False,
                                            "validators": [],
                                        },
                                        "properties": {
                                            "identifier": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "label.cs": "Identifikátor",
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String"
                                                    }
                                                },
                                                "label.en": "Identifier",
                                                "sample": {
                                                    "skip": False,
                                                    "faker": "isbn13",
                                                },
                                                "i18n.key": "identifier",
                                                "type": "keyword",
                                                "required": True,
                                            },
                                            "scheme": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                    ],
                                                },
                                                "label.cs": "Typ identifikátoru",
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "l10n.LocalizedEnum",
                                                        "arguments": [
                                                            'value_prefix="nr_metadata.documents"'
                                                        ],
                                                    }
                                                },
                                                "label.en": "Identifier type",
                                                "hint.cs": "Doporučujeme zadat alespoň jeden z typů identifikátorů.\nPokud potřebujete rozšířit nabídku typů identifikátorů, kontaktujte nás na support@narodni-repozitar.cz.\n",
                                                "enum": [
                                                    "orcid",
                                                    "scopusID",
                                                    "researcherID",
                                                    "czenasAutID",
                                                    "vedidk",
                                                    "institutionalID",
                                                    "ISNI",
                                                    "ROR",
                                                    "ICO",
                                                    "DOI",
                                                ],
                                                "hint.en": "We recommend providing at least one of the identifier types.\nIf you need to expand the range of identifier types, contact us at support@narodni-repozitar.cz.\n",
                                                "i18n.key": "identifier_type",
                                                "type": "keyword",
                                                "required": True,
                                            },
                                        },
                                        "ui": {
                                            "detail": "nr_authority_identifier",
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema",
                                                "imports": [
                                                    {
                                                        "import": "nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema"
                                                    }
                                                ],
                                                "generate": False,
                                            },
                                        },
                                        "type": "object",
                                    },
                                    "ui": {
                                        "marshmallow": {"field-class": "ma_fields.List"}
                                    },
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                            },
                            "ui": {
                                "detail": "contributor",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRContributorUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRContributorUISchema"
                                        }
                                    ],
                                },
                            },
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Contributors",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "resourceType": {
                        "marshmallow": {
                            "field-class": "ma_fields.Nested",
                            "schema-class": "nr_metadata.common.services.records.schema.NRResourceTypeVocabularySchema",  # NOSONAR
                            "imports": [
                                {
                                    "import": "nr_metadata.common.services.records.schema.NRResourceTypeVocabularySchema"
                                }
                            ],
                            "validators": [],
                        },
                        "label.cs": "Typ zdroje",
                        "properties": {
                            "id": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",
                                    "imports": [],
                                    "validators": [],
                                },
                                "ui": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    }
                                },
                                "sample": {"skip": True},
                                "type": "keyword",
                                "mapping": {
                                    "fields": {"text": {"type": "search_as_you_type"}}
                                },
                            },
                            "title": {
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                    "imports": [
                                        {
                                            "import": "invenio_vocabularies.services.schema.i18n_strings"
                                        }
                                    ],
                                    "validators": [],
                                    "field": "i18n_strings",
                                },
                                "ui": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                        "imports": [
                                            {
                                                "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                            }
                                        ],
                                        "generate": False,
                                        "field": "VocabularyI18nStrUIField()",
                                    }
                                },
                                "additionalProperties": {"type": "string"},
                                "propertyNames": {"pattern": "^[a-z]{2}$"},
                                "type": "object",
                                "mapping": {
                                    "properties": {
                                        "en": {"type": "search_as_you_type"}
                                    },
                                    "dynamic": True,
                                },
                            },
                            "type": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",
                                    "imports": [],
                                    "validators": [],
                                },
                                "ui": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    }
                                },
                                "type": "keyword",
                            },
                            "@v": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",
                                    "validators": [],
                                    "field-name": "_version",
                                    "imports": [],
                                },
                                "ui": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "field-name": "_version",
                                    }
                                },
                                "type": "keyword",
                            },
                        },
                        "ui": {
                            "detail": "vocabulary_item",
                            "edit": "vocabulary_item",
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.ui_schema.NRResourceTypeVocabularyUISchema",  # NOSONAR
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.ui_schema.NRResourceTypeVocabularyUISchema"
                                    }
                                ],
                            },
                        },
                        "pid-field": 'Vocabulary.pid.with_type_ctx("resource-types")',  # NOSONAR
                        "label.en": "Resource type",
                        "sample": [True, True, True],
                        "imports": [
                            {"import": "invenio_vocabularies.records.api.Vocabulary"},
                            {"import": "oarepo_runtime.relations.RelationsField"},
                            {"import": "oarepo_runtime.relations.PIDRelation"},
                            {"import": "oarepo_runtime.relations.InternalRelation"},
                            {"import": "invenio_vocabularies.records.api.Vocabulary"},
                        ],
                        "model": "vocabularies",
                        "schema-prefix": "Resourcetype",
                        "name": "resourceType",
                        "relation-class": "PIDRelation",
                        "keys": [
                            {"target": "id", "key": "id"},
                            {"target": "title", "key": "title"},
                            {"target": "type", "key": "type.id"},
                        ],
                        "model-class": "Vocabulary",
                        "relation-args": {
                            "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                            "pid_field": 'Vocabulary.pid.with_type_ctx("resource-types")',
                        },
                        "type": "relation",
                        "required": True,
                    },
                    "dateAvailable": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "validators": [
                                "mu_fields_edtf.EDTFValidator(types=(EDTFDate,))"
                            ],
                            "imports": [
                                {
                                    "import": "oarepo_runtime.ui.marshmallow",
                                    "alias": "l10n",
                                },
                                {"import": "edtf.Date", "alias": "EDTFDate"},  # NOSONAR
                                {
                                    "import": "marshmallow_utils.fields.edtfdatestring",  # NOSONAR
                                    "alias": "mu_fields_edtf",
                                },
                                {
                                    "import": "oarepo_runtime.ui.marshmallow",
                                    "alias": "l10n",
                                },
                                {"import": "edtf.Date", "alias": "EDTFDate"},
                                {
                                    "import": "marshmallow_utils.fields.edtfdatestring",
                                    "alias": "mu_fields_edtf",
                                },
                            ],
                        },
                        "label.cs": "Datum zveřejnění",
                        "ui": {"marshmallow": {"field-class": "l10n.LocalizedEDTF"}},
                        "label.en": "Date available",
                        "sample": {"skip": False, "faker": "date"},
                        "type": "edtf",
                    },
                    "dateModified": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "validators": [
                                "mu_fields_edtf.EDTFValidator(types=(EDTFDate,))"
                            ],
                            "imports": [
                                {
                                    "import": "oarepo_runtime.ui.marshmallow",
                                    "alias": "l10n",
                                },
                                {"import": "edtf.Date", "alias": "EDTFDate"},
                                {
                                    "import": "marshmallow_utils.fields.edtfdatestring",
                                    "alias": "mu_fields_edtf",
                                },
                                {
                                    "import": "oarepo_runtime.ui.marshmallow",
                                    "alias": "l10n",
                                },
                                {"import": "edtf.Date", "alias": "EDTFDate"},
                                {
                                    "import": "marshmallow_utils.fields.edtfdatestring",
                                    "alias": "mu_fields_edtf",
                                },
                            ],
                        },
                        "label.cs": "Datum změny zdroje",
                        "ui": {"marshmallow": {"field-class": "l10n.LocalizedEDTF"}},
                        "label.en": "Date modified",
                        "sample": {"skip": False, "faker": "date"},
                        "type": "edtf",
                    },
                    "subjects": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Klíčová slova",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRSubjectSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRSubjectSchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Klíčové slovo",
                            "properties": {
                                "subjectScheme": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "sample": [True, True, True],
                                    "type": "keyword",
                                },
                                "subject": {
                                    "marshmallow": {
                                        "field-class": "MultilingualField",
                                        "imports": [
                                            {
                                                "import": "oarepo_runtime.i18n.schema.MultilingualField"  # NOSONAR
                                            }
                                        ],
                                        "validators": [],
                                    },
                                    "label.cs": "Klíčová slova",
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "I18nStrField",
                                            "schema-class": None,
                                            "imports": [
                                                {
                                                    "import": "oarepo_runtime.i18n.schema.I18nStrField"
                                                }
                                            ],
                                            "generate": False,
                                            "validators": [],
                                        },
                                        "properties": {
                                            "lang": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String"
                                                    }
                                                },
                                                "type": "keyword",
                                            },
                                            "value": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String"
                                                    }
                                                },
                                                "type": "fulltext+keyword",
                                            },
                                        },
                                        "ui": {
                                            "detail": "multilingual",
                                            "marshmallow": {
                                                "field-class": "I18nStrUIField",
                                                "schema-class": None,
                                                "imports": [
                                                    {
                                                        "import": "oarepo_runtime.i18n.ui_schema.I18nStrUIField"
                                                    }
                                                ],
                                            },
                                        },
                                        "sample": {"skip": False},
                                        "type": "i18nStr",
                                    },
                                    "ui": {
                                        "detail": "string",
                                        "marshmallow": {
                                            "field-class": "MultilingualUIField",
                                            "imports": [
                                                {
                                                    "import": "oarepo_runtime.i18n.ui_schema.I18nStrUIField"
                                                },
                                                {
                                                    "import": "oarepo_runtime.i18n.ui_schema.MultilingualUIField"  # NOSONAR
                                                },
                                            ],
                                            "field": "I18nStrUIField()",
                                        },
                                    },
                                    "label.en": "Keywords",
                                    "type": "array",
                                    "required": True,
                                },
                                "valueURI": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "sample": {"skip": False, "faker": "url"},
                                    "type": "url",
                                },
                                "classificationCode": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "keyword",
                                },
                            },
                            "ui": {
                                "detail": "subject",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRSubjectUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRSubjectUISchema"
                                        }
                                    ],
                                },
                            },
                            "label.en": "Keyword",
                            "type": "object",
                        },
                        "ui": {
                            "marshmallow": {
                                "field-class": "NRSubjectListField",
                                "imports": [
                                    {
                                        "import": "nr_metadata.ui_schema.subjects.NRSubjectListField"
                                    }
                                ],
                            }
                        },
                        "label.en": "Keywords",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "publishers": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Vydavatelé",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.String",
                                "validators": [],
                                "imports": [],
                            },
                            "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                            "sample": {"skip": False, "faker": "company"},
                            "type": "fulltext",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Publishers",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "subjectCategories": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Oborové třídění",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRSubjectCategoryVocabularySchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRSubjectCategoryVocabularySchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Oborové třídění",
                            "properties": {
                                "id": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "imports": [],
                                            "validators": [],
                                        }
                                    },
                                    "sample": {"skip": True},
                                    "type": "keyword",
                                    "mapping": {
                                        "fields": {
                                            "text": {"type": "search_as_you_type"}
                                        }
                                    },
                                },
                                "title": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                        "imports": [
                                            {
                                                "import": "invenio_vocabularies.services.schema.i18n_strings"
                                            }
                                        ],
                                        "validators": [],
                                        "field": "i18n_strings",
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                            "imports": [
                                                {
                                                    "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                }
                                            ],
                                            "generate": False,
                                            "field": "VocabularyI18nStrUIField()",
                                        }
                                    },
                                    "additionalProperties": {"type": "string"},
                                    "propertyNames": {"pattern": "^[a-z]{2}$"},
                                    "type": "object",
                                    "mapping": {
                                        "properties": {
                                            "en": {"type": "search_as_you_type"}
                                        },
                                        "dynamic": True,
                                    },
                                },
                                "type": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "imports": [],
                                            "validators": [],
                                        }
                                    },
                                    "type": "keyword",
                                },
                                "@v": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "field-name": "_version",
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "field-name": "_version",
                                        }
                                    },
                                    "type": "keyword",
                                },
                            },
                            "ui": {
                                "detail": "vocabulary_item",
                                "edit": "vocabulary_item",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRSubjectCategoryVocabularyUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRSubjectCategoryVocabularyUISchema"
                                        }
                                    ],
                                },
                            },
                            "pid-field": 'Vocabulary.pid.with_type_ctx("subject-categories")',
                            "label.en": "Subject categories",
                            "imports": [
                                {
                                    "import": "invenio_vocabularies.records.api.Vocabulary"
                                },
                                {"import": "oarepo_runtime.relations.RelationsField"},
                                {"import": "oarepo_runtime.relations.PIDRelation"},
                                {"import": "oarepo_runtime.relations.InternalRelation"},
                                {
                                    "import": "invenio_vocabularies.records.api.Vocabulary"
                                },
                            ],
                            "model": "vocabularies",
                            "schema-prefix": "SubjectcategoriesItem",
                            "name": "subjectCategories_item",
                            "relation-class": "PIDRelation",
                            "keys": [
                                {"target": "id", "key": "id"},
                                {"target": "title", "key": "title"},
                                {"target": "type", "key": "type.id"},
                            ],
                            "model-class": "Vocabulary",
                            "relation-args": {
                                "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                                "pid_field": 'Vocabulary.pid.with_type_ctx("subject-categories")',
                            },
                            "type": "relation",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Subject categories",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "languages": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Jazyk",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRLanguageVocabularySchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRLanguageVocabularySchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Jazyk",
                            "properties": {
                                "id": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "imports": [],
                                            "validators": [],
                                        }
                                    },
                                    "sample": {"skip": True},
                                    "type": "keyword",
                                    "mapping": {
                                        "fields": {
                                            "text": {"type": "search_as_you_type"}
                                        }
                                    },
                                },
                                "title": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                        "imports": [
                                            {
                                                "import": "invenio_vocabularies.services.schema.i18n_strings"
                                            }
                                        ],
                                        "validators": [],
                                        "field": "i18n_strings",
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                            "imports": [
                                                {
                                                    "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                }
                                            ],
                                            "generate": False,
                                            "field": "VocabularyI18nStrUIField()",
                                        }
                                    },
                                    "additionalProperties": {"type": "string"},
                                    "propertyNames": {"pattern": "^[a-z]{2}$"},
                                    "type": "object",
                                    "mapping": {
                                        "properties": {
                                            "en": {"type": "search_as_you_type"}
                                        },
                                        "dynamic": True,
                                    },
                                },
                                "type": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "imports": [],
                                            "validators": [],
                                        }
                                    },
                                    "type": "keyword",
                                },
                                "@v": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "field-name": "_version",
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "field-name": "_version",
                                        }
                                    },
                                    "type": "keyword",
                                },
                            },
                            "ui": {
                                "detail": "vocabulary_item",
                                "edit": "vocabulary_item",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRLanguageVocabularyUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRLanguageVocabularyUISchema"
                                        }
                                    ],
                                },
                            },
                            "pid-field": 'Vocabulary.pid.with_type_ctx("languages")',
                            "label.en": "Language",
                            "sample": [True, True, True, True, True],
                            "imports": [
                                {
                                    "import": "invenio_vocabularies.records.api.Vocabulary"
                                },
                                {"import": "oarepo_runtime.relations.RelationsField"},
                                {"import": "oarepo_runtime.relations.PIDRelation"},
                                {"import": "oarepo_runtime.relations.InternalRelation"},
                                {
                                    "import": "invenio_vocabularies.records.api.Vocabulary"
                                },
                            ],
                            "model": "vocabularies",
                            "schema-prefix": "LanguagesItem",
                            "name": "languages_item",
                            "relation-class": "PIDRelation",
                            "keys": [
                                {"target": "id", "key": "id"},
                                {"target": "title", "key": "title"},
                                {"target": "type", "key": "type.id"},
                            ],
                            "model-class": "Vocabulary",
                            "relation-args": {
                                "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                                "pid_field": 'Vocabulary.pid.with_type_ctx("languages")',
                            },
                            "type": "relation",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Language",
                        "uniqueItems": True,
                        "minItems": 1,
                        "type": "array",
                        "required": True,
                    },
                    "notes": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Poznámky",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.String",
                                "validators": [],
                                "imports": [],
                            },
                            "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                            "type": "fulltext",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Notes",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "abstract": {
                        "marshmallow": {
                            "field-class": "MultilingualField",
                            "imports": [
                                {
                                    "import": "oarepo_runtime.i18n.schema.MultilingualField"
                                }
                            ],
                            "validators": [],
                        },
                        "label.cs": "Abstrakt",
                        "items": {
                            "marshmallow": {
                                "field-class": "I18nStrField",
                                "schema-class": None,
                                "imports": [
                                    {
                                        "import": "oarepo_runtime.i18n.schema.I18nStrField"
                                    }
                                ],
                                "generate": False,
                                "validators": [],
                            },
                            "properties": {
                                "lang": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "keyword",
                                },
                                "value": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "fulltext+keyword",
                                },
                            },
                            "ui": {
                                "detail": "multilingual",
                                "marshmallow": {
                                    "field-class": "I18nStrUIField",
                                    "schema-class": None,
                                    "imports": [
                                        {
                                            "import": "oarepo_runtime.i18n.ui_schema.I18nStrUIField"
                                        }
                                    ],
                                },
                            },
                            "sample": {"skip": False},
                            "type": "i18nStr",
                        },
                        "ui": {
                            "detail": "multilingual",
                            "marshmallow": {
                                "field-class": "MultilingualUIField",
                                "imports": [
                                    {
                                        "import": "oarepo_runtime.i18n.ui_schema.MultilingualUIField"
                                    }
                                ],
                            },
                        },
                        "label.en": "Abstract",
                        "type": "array",
                    },
                    "methods": {
                        "marshmallow": {
                            "field-class": "MultilingualField",
                            "imports": [
                                {
                                    "import": "oarepo_runtime.i18n.schema.MultilingualField"
                                }
                            ],
                            "validators": [],
                        },
                        "label.cs": "Metodologie",
                        "items": {
                            "marshmallow": {
                                "field-class": "I18nStrField",
                                "schema-class": None,
                                "imports": [
                                    {
                                        "import": "oarepo_runtime.i18n.schema.I18nStrField"
                                    }
                                ],
                                "generate": False,
                                "validators": [],
                            },
                            "properties": {
                                "lang": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "keyword",
                                },
                                "value": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "fulltext+keyword",
                                },
                            },
                            "ui": {
                                "detail": "multilingual",
                                "marshmallow": {
                                    "field-class": "I18nStrUIField",
                                    "schema-class": None,
                                    "imports": [
                                        {
                                            "import": "oarepo_runtime.i18n.ui_schema.I18nStrUIField"
                                        }
                                    ],
                                },
                            },
                            "sample": {"skip": False},
                            "type": "i18nStr",
                        },
                        "ui": {
                            "detail": "multilingual",
                            "marshmallow": {
                                "field-class": "MultilingualUIField",
                                "imports": [
                                    {
                                        "import": "oarepo_runtime.i18n.ui_schema.MultilingualUIField"
                                    }
                                ],
                            },
                        },
                        "label.en": "Methods",
                        "type": "array",
                    },
                    "technicalInfo": {
                        "marshmallow": {
                            "field-class": "MultilingualField",
                            "imports": [
                                {
                                    "import": "oarepo_runtime.i18n.schema.MultilingualField"
                                }
                            ],
                            "validators": [],
                        },
                        "label.cs": "Technické informace",
                        "items": {
                            "marshmallow": {
                                "field-class": "I18nStrField",
                                "schema-class": None,
                                "imports": [
                                    {
                                        "import": "oarepo_runtime.i18n.schema.I18nStrField"
                                    }
                                ],
                                "generate": False,
                                "validators": [],
                            },
                            "properties": {
                                "lang": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "keyword",
                                },
                                "value": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "fulltext+keyword",
                                },
                            },
                            "ui": {
                                "detail": "multilingual",
                                "marshmallow": {
                                    "field-class": "I18nStrUIField",
                                    "schema-class": None,
                                    "imports": [
                                        {
                                            "import": "oarepo_runtime.i18n.ui_schema.I18nStrUIField"
                                        }
                                    ],
                                },
                            },
                            "sample": {"skip": False},
                            "type": "i18nStr",
                        },
                        "ui": {
                            "detail": "multilingual",
                            "marshmallow": {
                                "field-class": "MultilingualUIField",
                                "imports": [
                                    {
                                        "import": "oarepo_runtime.i18n.ui_schema.MultilingualUIField"
                                    }
                                ],
                            },
                        },
                        "label.en": "Technical information",
                        "type": "array",
                    },
                    "rights": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Autoři",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRLicenseVocabularySchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRLicenseVocabularySchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Licence",
                            "properties": {
                                "id": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "imports": [],
                                            "validators": [],
                                        }
                                    },
                                    "sample": {"skip": True},
                                    "type": "keyword",
                                    "mapping": {
                                        "fields": {
                                            "text": {"type": "search_as_you_type"}
                                        }
                                    },
                                },
                                "title": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                        "imports": [
                                            {
                                                "import": "invenio_vocabularies.services.schema.i18n_strings"
                                            }
                                        ],
                                        "validators": [],
                                        "field": "i18n_strings",
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                            "imports": [
                                                {
                                                    "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                }
                                            ],
                                            "generate": False,
                                            "field": "VocabularyI18nStrUIField()",
                                        }
                                    },
                                    "additionalProperties": {"type": "string"},
                                    "propertyNames": {"pattern": "^[a-z]{2}$"},
                                    "type": "object",
                                    "mapping": {
                                        "properties": {
                                            "en": {"type": "search_as_you_type"}
                                        },
                                        "dynamic": True,
                                    },
                                },
                                "type": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "imports": [],
                                            "validators": [],
                                        }
                                    },
                                    "type": "keyword",
                                },
                                "@v": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "field-name": "_version",
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "field-name": "_version",
                                        }
                                    },
                                    "type": "keyword",
                                },
                            },
                            "ui": {
                                "detail": "vocabulary_item",
                                "edit": "vocabulary_item",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRLicenseVocabularyUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRLicenseVocabularyUISchema"
                                        }
                                    ],
                                },
                            },
                            "pid-field": 'Vocabulary.pid.with_type_ctx("licenses")',
                            "label.en": "License",
                            "sample": [True, True, True, True, True, True],
                            "imports": [
                                {
                                    "import": "invenio_vocabularies.records.api.Vocabulary"
                                },
                                {"import": "oarepo_runtime.relations.RelationsField"},
                                {"import": "oarepo_runtime.relations.PIDRelation"},
                                {"import": "oarepo_runtime.relations.InternalRelation"},
                                {
                                    "import": "invenio_vocabularies.records.api.Vocabulary"
                                },
                            ],
                            "model": "vocabularies",
                            "schema-prefix": "RightsItem",
                            "name": "rights_item",
                            "relation-class": "PIDRelation",
                            "keys": [
                                {"target": "id", "key": "id"},
                                {"target": "title", "key": "title"},
                                {"target": "type", "key": "type.id"},
                            ],
                            "model-class": "Vocabulary",
                            "relation-args": {
                                "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                                "pid_field": 'Vocabulary.pid.with_type_ctx("licenses")',
                            },
                            "type": "relation",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Authors",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "accessRights": {
                        "marshmallow": {
                            "field-class": "ma_fields.Nested",
                            "schema-class": "nr_metadata.common.services.records.schema.NRAccessRightsVocabularySchema",
                            "imports": [
                                {
                                    "import": "nr_metadata.common.services.records.schema.NRAccessRightsVocabularySchema"
                                }
                            ],
                            "validators": [],
                        },
                        "label.cs": "Přístupová práva",
                        "properties": {
                            "id": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",
                                    "imports": [],
                                    "validators": [],
                                },
                                "ui": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    }
                                },
                                "sample": {"skip": True},
                                "type": "keyword",
                                "mapping": {
                                    "fields": {"text": {"type": "search_as_you_type"}}
                                },
                            },
                            "title": {
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                    "imports": [
                                        {
                                            "import": "invenio_vocabularies.services.schema.i18n_strings"
                                        }
                                    ],
                                    "validators": [],
                                    "field": "i18n_strings",
                                },
                                "ui": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                        "imports": [
                                            {
                                                "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                            }
                                        ],
                                        "generate": False,
                                        "field": "VocabularyI18nStrUIField()",
                                    }
                                },
                                "additionalProperties": {"type": "string"},
                                "propertyNames": {"pattern": "^[a-z]{2}$"},
                                "type": "object",
                                "mapping": {
                                    "properties": {
                                        "en": {"type": "search_as_you_type"}
                                    },
                                    "dynamic": True,
                                },
                            },
                            "type": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",
                                    "imports": [],
                                    "validators": [],
                                },
                                "ui": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "imports": [],
                                        "validators": [],
                                    }
                                },
                                "type": "keyword",
                            },
                            "@v": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",
                                    "validators": [],
                                    "field-name": "_version",
                                    "imports": [],
                                },
                                "ui": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "field-name": "_version",
                                    }
                                },
                                "type": "keyword",
                            },
                        },
                        "ui": {
                            "detail": "vocabulary_item",
                            "edit": "vocabulary_item",
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.ui_schema.NRAccessRightsVocabularyUISchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.ui_schema.NRAccessRightsVocabularyUISchema"
                                    }
                                ],
                            },
                        },
                        "pid-field": 'Vocabulary.pid.with_type_ctx("access-rights")',
                        "label.en": "Access rights",
                        "sample": [True, True, True, True],
                        "imports": [
                            {"import": "invenio_vocabularies.records.api.Vocabulary"},
                            {"import": "oarepo_runtime.relations.RelationsField"},
                            {"import": "oarepo_runtime.relations.PIDRelation"},
                            {"import": "oarepo_runtime.relations.InternalRelation"},
                            {"import": "invenio_vocabularies.records.api.Vocabulary"},
                        ],
                        "model": "vocabularies",
                        "schema-prefix": "Accessrights",
                        "name": "accessRights",
                        "relation-class": "PIDRelation",
                        "keys": [
                            {"target": "id", "key": "id"},
                            {"target": "title", "key": "title"},
                            {"target": "type", "key": "type.id"},
                        ],
                        "model-class": "Vocabulary",
                        "relation-args": {
                            "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                            "pid_field": 'Vocabulary.pid.with_type_ctx("access-rights")',
                        },
                        "type": "relation",
                    },
                    "relatedItems": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Vazba na/z dalších zdrojů:",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRRelatedItemSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRRelatedItemSchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Vazba na/z dalších zdrojů:",
                            "properties": {
                                "itemTitle": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Název",
                                    "description": "název propojeného dokumentu",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Title",
                                    "type": "fulltext",
                                    "required": True,
                                },
                                "itemCreators": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.List",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Autoři",
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.schema.NRAuthoritySchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.schema.NRAuthoritySchema"
                                                }
                                            ],
                                            "validators": [],
                                        },
                                        "properties": {
                                            "affiliations": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.List",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "label.cs": "Afiliace",
                                                "items": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "nr_metadata.common.services.records.schema.NRAffiliationVocabularySchema",
                                                        "imports": [
                                                            {
                                                                "import": "nr_metadata.common.services.records.schema.NRAffiliationVocabularySchema"
                                                            }
                                                        ],
                                                        "validators": [],
                                                    },
                                                    "label.cs": "Afiliace",
                                                    "properties": {
                                                        "id": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "imports": [],
                                                                "validators": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String",
                                                                    "imports": [],
                                                                    "validators": [],
                                                                }
                                                            },
                                                            "sample": {"skip": True},
                                                            "type": "keyword",
                                                            "mapping": {
                                                                "fields": {
                                                                    "text": {
                                                                        "type": "search_as_you_type"
                                                                    }
                                                                }
                                                            },
                                                        },
                                                        "title": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Nested",
                                                                "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                                "imports": [
                                                                    {
                                                                        "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                                    }
                                                                ],
                                                                "validators": [],
                                                                "field": "i18n_strings",
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.Nested",
                                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                                    "imports": [
                                                                        {
                                                                            "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                                        }
                                                                    ],
                                                                    "generate": False,
                                                                    "field": "VocabularyI18nStrUIField()",
                                                                }
                                                            },
                                                            "additionalProperties": {
                                                                "type": "string"
                                                            },
                                                            "propertyNames": {
                                                                "pattern": "^[a-z]{2}$"
                                                            },
                                                            "type": "object",
                                                            "mapping": {
                                                                "properties": {
                                                                    "en": {
                                                                        "type": "search_as_you_type"
                                                                    }
                                                                },
                                                                "dynamic": True,
                                                            },
                                                        },
                                                        "type": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "imports": [],
                                                                "validators": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String",
                                                                    "imports": [],
                                                                    "validators": [],
                                                                }
                                                            },
                                                            "type": "keyword",
                                                        },
                                                        "hierarchy": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Nested",
                                                                "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                                "imports": [
                                                                    {
                                                                        "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                                    }
                                                                ],
                                                                "generate": False,
                                                                "validators": [],
                                                            },
                                                            "properties": {
                                                                "parent": {
                                                                    "marshmallow": {
                                                                        "field-class": "ma_fields.String",
                                                                        "validators": [],
                                                                        "imports": [],
                                                                    },
                                                                    "ui": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.String"
                                                                        }
                                                                    },
                                                                    "type": "keyword",
                                                                },
                                                                "level": {
                                                                    "marshmallow": {
                                                                        "field-class": "ma_fields.Integer",
                                                                        "validators": [],
                                                                        "imports": [],
                                                                    },
                                                                    "ui": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.Integer"
                                                                        }
                                                                    },
                                                                    "type": "integer",
                                                                },
                                                                "title": {
                                                                    "marshmallow": {
                                                                        "field-class": "ma_fields.List",
                                                                        "validators": [],
                                                                        "imports": [],
                                                                    },
                                                                    "items": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.Nested",
                                                                            "schema-class": "nr_metadata.documents.services.records.schema.TitleItemSchema",
                                                                            "validators": [],
                                                                            "field": "i18n_strings",
                                                                            "imports": [],
                                                                        },
                                                                        "ui": {
                                                                            "marshmallow": {
                                                                                "field-class": "ma_fields.Nested",
                                                                                "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleItemUISchema",
                                                                                "field": "i18n_strings",
                                                                            }
                                                                        },
                                                                        "additionalProperties": {
                                                                            "type": "string"
                                                                        },
                                                                        "propertyNames": {
                                                                            "pattern": "^[a-z]{2}$"
                                                                        },
                                                                        "type": "object",
                                                                        "mapping": {
                                                                            "dynamic": True
                                                                        },
                                                                    },
                                                                    "ui": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.List"
                                                                        }
                                                                    },
                                                                    "type": "array",
                                                                },
                                                                "ancestors": {
                                                                    "marshmallow": {
                                                                        "field-class": "ma_fields.List",
                                                                        "validators": [],
                                                                        "imports": [],
                                                                    },
                                                                    "items": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.String",
                                                                            "validators": [],
                                                                            "imports": [],
                                                                        },
                                                                        "ui": {
                                                                            "marshmallow": {
                                                                                "field-class": "ma_fields.String"
                                                                            }
                                                                        },
                                                                        "type": "keyword",
                                                                    },
                                                                    "ui": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.List"
                                                                        }
                                                                    },
                                                                    "type": "array",
                                                                },
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.Nested",
                                                                    "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                                    "generate": False,
                                                                }
                                                            },
                                                            "type": "object",
                                                        },
                                                        "@v": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "validators": [],
                                                                "field-name": "_version",
                                                                "imports": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String",
                                                                    "field-name": "_version",
                                                                }
                                                            },
                                                            "type": "keyword",
                                                        },
                                                    },
                                                    "ui": {
                                                        "detail": "taxonomy_item",
                                                        "edit": "taxonomy_item",
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Nested",
                                                            "schema-class": "nr_metadata.common.services.records.ui_schema.NRAffiliationVocabularyUISchema",
                                                            "imports": [
                                                                {
                                                                    "import": "nr_metadata.common.services.records.ui_schema.NRAffiliationVocabularyUISchema"
                                                                }
                                                            ],
                                                        },
                                                    },
                                                    "pid-field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                                    "label.en": "Affiliation",
                                                    "sample": {
                                                        "skip": False,
                                                        "faker": "company",
                                                    },
                                                    "imports": [
                                                        {
                                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.relations.RelationsField"
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.relations.PIDRelation"
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.relations.InternalRelation"
                                                        },
                                                        {
                                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                                        },
                                                    ],
                                                    "model": "vocabularies",
                                                    "hint.cs": "Uveďte instituci/instituce, pod jejíž záštitou jste se na tvorbě objektu podíleli.",
                                                    "schema-prefix": "AffiliationsItem",
                                                    "name": "affiliations_item",
                                                    "relation-class": "PIDRelation",
                                                    "keys": [
                                                        {"target": "id", "key": "id"},
                                                        {
                                                            "target": "title",
                                                            "key": "title",
                                                        },
                                                        {
                                                            "target": "type",
                                                            "key": "type.id",
                                                        },
                                                        {
                                                            "model": {
                                                                "properties": {
                                                                    "parent": {
                                                                        "type": "keyword"
                                                                    },
                                                                    "level": {
                                                                        "type": "integer"
                                                                    },
                                                                    "title": {
                                                                        "items": {
                                                                            "ui": {
                                                                                "marshmallow": {
                                                                                    "field": "i18n_strings"
                                                                                }
                                                                            },
                                                                            "marshmallow": {
                                                                                "field": "i18n_strings"
                                                                            },
                                                                            "additionalProperties": {
                                                                                "type": "string"
                                                                            },
                                                                            "propertyNames": {
                                                                                "pattern": "^[a-z]{2}$"
                                                                            },
                                                                            "type": "object",
                                                                            "mapping": {
                                                                                "dynamic": True
                                                                            },
                                                                        },
                                                                        "type": "array",
                                                                    },
                                                                    "ancestors": {
                                                                        "items": {
                                                                            "type": "keyword"
                                                                        },
                                                                        "type": "array",
                                                                    },
                                                                },
                                                                "ui": {
                                                                    "marshmallow": {
                                                                        "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                                        "generate": False,
                                                                    }
                                                                },
                                                                "marshmallow": {
                                                                    "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                                    "imports": [
                                                                        {
                                                                            "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                                        }
                                                                    ],
                                                                    "generate": False,
                                                                },
                                                                "type": "object",
                                                            },
                                                            "target": "hierarchy",
                                                            "key": "hierarchy",
                                                        },
                                                    ],
                                                    "model-class": "Vocabulary",
                                                    "relation-args": {
                                                        "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}, 'hierarchy']",
                                                        "pid_field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                                    },
                                                    "type": "relation",
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.List"
                                                    }
                                                },
                                                "label.en": "Affiliation",
                                                "uniqueItems": True,
                                                "type": "array",
                                            },
                                            "nameType": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                    ],
                                                },
                                                "label.cs": "Typ",
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "l10n.LocalizedEnum",
                                                        "arguments": [
                                                            'value_prefix="nr_metadata.documents"'
                                                        ],
                                                    }
                                                },
                                                "label.en": "Type",
                                                "sample": [True, True],
                                                "hint.cs": "Jako tvůrce je možné označit osobu nebo instituci.",
                                                "enum": ["Organizational", "Personal"],
                                                "hint.en": "It is possible to designate a person or an institution as the creator/contributor.",
                                                "type": "keyword",
                                            },
                                            "fullName": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String"
                                                    }
                                                },
                                                "sample": {
                                                    "skip": False,
                                                    "faker": "name",
                                                },
                                                "type": "keyword",
                                                "required": True,
                                            },
                                            "authorityIdentifiers": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.List",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "items": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema",
                                                        "imports": [
                                                            {
                                                                "import": "nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema"
                                                            }
                                                        ],
                                                        "generate": False,
                                                        "validators": [],
                                                    },
                                                    "properties": {
                                                        "identifier": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "validators": [],
                                                                "imports": [],
                                                            },
                                                            "label.cs": "Identifikátor",
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String"
                                                                }
                                                            },
                                                            "label.en": "Identifier",
                                                            "sample": {
                                                                "skip": False,
                                                                "faker": "isbn13",
                                                            },
                                                            "i18n.key": "identifier",
                                                            "type": "keyword",
                                                            "required": True,
                                                        },
                                                        "scheme": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "validators": [],
                                                                "imports": [
                                                                    {
                                                                        "import": "oarepo_runtime.ui.marshmallow",
                                                                        "alias": "l10n",
                                                                    },
                                                                    {
                                                                        "import": "oarepo_runtime.ui.marshmallow",
                                                                        "alias": "l10n",
                                                                    },
                                                                ],
                                                            },
                                                            "label.cs": "Typ identifikátoru",
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "l10n.LocalizedEnum",
                                                                    "arguments": [
                                                                        'value_prefix="nr_metadata.documents"'
                                                                    ],
                                                                }
                                                            },
                                                            "label.en": "Identifier type",
                                                            "hint.cs": "Doporučujeme zadat alespoň jeden z typů identifikátorů.\nPokud potřebujete rozšířit nabídku typů identifikátorů, kontaktujte nás na support@narodni-repozitar.cz.\n",
                                                            "enum": [
                                                                "orcid",
                                                                "scopusID",
                                                                "researcherID",
                                                                "czenasAutID",
                                                                "vedidk",
                                                                "institutionalID",
                                                                "ISNI",
                                                                "ROR",
                                                                "ICO",
                                                                "DOI",
                                                            ],
                                                            "hint.en": "We recommend providing at least one of the identifier types.\nIf you need to expand the range of identifier types, contact us at support@narodni-repozitar.cz.\n",
                                                            "i18n.key": "identifier_type",
                                                            "type": "keyword",
                                                            "required": True,
                                                        },
                                                    },
                                                    "ui": {
                                                        "detail": "nr_authority_identifier",
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Nested",
                                                            "schema-class": "nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema",
                                                            "imports": [
                                                                {
                                                                    "import": "nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema"
                                                                }
                                                            ],
                                                            "generate": False,
                                                        },
                                                    },
                                                    "type": "object",
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.List"
                                                    }
                                                },
                                                "uniqueItems": True,
                                                "type": "array",
                                            },
                                        },
                                        "ui": {
                                            "detail": "creator",
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "nr_metadata.common.services.records.ui_schema.NRAuthorityUIUISchema",
                                                "imports": [
                                                    {
                                                        "import": "nr_metadata.common.services.records.ui_schema.NRAuthorityUIUISchema"
                                                    }
                                                ],
                                            },
                                        },
                                        "type": "object",
                                    },
                                    "ui": {
                                        "marshmallow": {"field-class": "ma_fields.List"}
                                    },
                                    "label.en": "Authors",
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                                "itemContributors": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.List",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Přispěvatelé",
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.schema.NRAuthoritySchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.schema.NRAuthoritySchema"
                                                }
                                            ],
                                            "validators": [],
                                        },
                                        "properties": {
                                            "role": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "nr_metadata.common.services.records.schema.NRAuthorityRoleVocabularySchema",
                                                    "imports": [
                                                        {
                                                            "import": "nr_metadata.common.services.records.schema.NRAuthorityRoleVocabularySchema"
                                                        }
                                                    ],
                                                    "validators": [],
                                                },
                                                "label.cs": "Role přispěvatele",
                                                "properties": {
                                                    "id": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "imports": [],
                                                            "validators": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "imports": [],
                                                                "validators": [],
                                                            }
                                                        },
                                                        "sample": {"skip": True},
                                                        "type": "keyword",
                                                        "mapping": {
                                                            "fields": {
                                                                "text": {
                                                                    "type": "search_as_you_type"
                                                                }
                                                            }
                                                        },
                                                    },
                                                    "title": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Nested",
                                                            "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                            "imports": [
                                                                {
                                                                    "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                                }
                                                            ],
                                                            "validators": [],
                                                            "field": "i18n_strings",
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Nested",
                                                                "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                                "imports": [
                                                                    {
                                                                        "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                                    }
                                                                ],
                                                                "generate": False,
                                                                "field": "VocabularyI18nStrUIField()",
                                                            }
                                                        },
                                                        "additionalProperties": {
                                                            "type": "string"
                                                        },
                                                        "propertyNames": {
                                                            "pattern": "^[a-z]{2}$"
                                                        },
                                                        "type": "object",
                                                        "mapping": {
                                                            "properties": {
                                                                "en": {
                                                                    "type": "search_as_you_type"
                                                                }
                                                            },
                                                            "dynamic": True,
                                                        },
                                                    },
                                                    "type": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "imports": [],
                                                            "validators": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "imports": [],
                                                                "validators": [],
                                                            }
                                                        },
                                                        "type": "keyword",
                                                    },
                                                    "@v": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "validators": [],
                                                            "field-name": "_version",
                                                            "imports": [],
                                                        },
                                                        "ui": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "field-name": "_version",
                                                            }
                                                        },
                                                        "type": "keyword",
                                                    },
                                                },
                                                "ui": {
                                                    "detail": "vocabulary_item",
                                                    "edit": "vocabulary_item",
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "nr_metadata.common.services.records.ui_schema.NRAuthorityRoleVocabularyUISchema",
                                                        "imports": [
                                                            {
                                                                "import": "nr_metadata.common.services.records.ui_schema.NRAuthorityRoleVocabularyUISchema"
                                                            }
                                                        ],
                                                    },
                                                },
                                                "pid-field": 'Vocabulary.pid.with_type_ctx("contributor-roles")',
                                                "label.en": "Contributor's role",
                                                "imports": [
                                                    {
                                                        "import": "invenio_vocabularies.records.api.Vocabulary"
                                                    },
                                                    {
                                                        "import": "oarepo_runtime.relations.RelationsField"
                                                    },
                                                    {
                                                        "import": "oarepo_runtime.relations.PIDRelation"
                                                    },
                                                    {
                                                        "import": "oarepo_runtime.relations.InternalRelation"
                                                    },
                                                    {
                                                        "import": "invenio_vocabularies.records.api.Vocabulary"
                                                    },
                                                ],
                                                "model": "vocabularies",
                                                "schema-prefix": "Role",
                                                "name": "role",
                                                "relation-class": "PIDRelation",
                                                "keys": [
                                                    {"target": "id", "key": "id"},
                                                    {"target": "title", "key": "title"},
                                                    {
                                                        "target": "type",
                                                        "key": "type.id",
                                                    },
                                                ],
                                                "model-class": "Vocabulary",
                                                "relation-args": {
                                                    "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                                                    "pid_field": 'Vocabulary.pid.with_type_ctx("contributor-roles")',
                                                },
                                                "type": "relation",
                                            },
                                            "affiliations": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.List",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "label.cs": "Afiliace",
                                                "items": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "nr_metadata.common.services.records.schema.NRAffiliationVocabularySchema",
                                                        "imports": [
                                                            {
                                                                "import": "nr_metadata.common.services.records.schema.NRAffiliationVocabularySchema"
                                                            }
                                                        ],
                                                        "validators": [],
                                                    },
                                                    "label.cs": "Afiliace",
                                                    "properties": {
                                                        "id": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "imports": [],
                                                                "validators": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String",
                                                                    "imports": [],
                                                                    "validators": [],
                                                                }
                                                            },
                                                            "sample": {"skip": True},
                                                            "type": "keyword",
                                                            "mapping": {
                                                                "fields": {
                                                                    "text": {
                                                                        "type": "search_as_you_type"
                                                                    }
                                                                }
                                                            },
                                                        },
                                                        "title": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Nested",
                                                                "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                                "imports": [
                                                                    {
                                                                        "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                                    }
                                                                ],
                                                                "validators": [],
                                                                "field": "i18n_strings",
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.Nested",
                                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                                    "imports": [
                                                                        {
                                                                            "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                                        }
                                                                    ],
                                                                    "generate": False,
                                                                    "field": "VocabularyI18nStrUIField()",
                                                                }
                                                            },
                                                            "additionalProperties": {
                                                                "type": "string"
                                                            },
                                                            "propertyNames": {
                                                                "pattern": "^[a-z]{2}$"
                                                            },
                                                            "type": "object",
                                                            "mapping": {
                                                                "properties": {
                                                                    "en": {
                                                                        "type": "search_as_you_type"
                                                                    }
                                                                },
                                                                "dynamic": True,
                                                            },
                                                        },
                                                        "type": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "imports": [],
                                                                "validators": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String",
                                                                    "imports": [],
                                                                    "validators": [],
                                                                }
                                                            },
                                                            "type": "keyword",
                                                        },
                                                        "hierarchy": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.Nested",
                                                                "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                                "imports": [
                                                                    {
                                                                        "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                                    }
                                                                ],
                                                                "generate": False,
                                                                "validators": [],
                                                            },
                                                            "properties": {
                                                                "parent": {
                                                                    "marshmallow": {
                                                                        "field-class": "ma_fields.String",
                                                                        "validators": [],
                                                                        "imports": [],
                                                                    },
                                                                    "ui": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.String"
                                                                        }
                                                                    },
                                                                    "type": "keyword",
                                                                },
                                                                "level": {
                                                                    "marshmallow": {
                                                                        "field-class": "ma_fields.Integer",
                                                                        "validators": [],
                                                                        "imports": [],
                                                                    },
                                                                    "ui": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.Integer"
                                                                        }
                                                                    },
                                                                    "type": "integer",
                                                                },
                                                                "title": {
                                                                    "marshmallow": {
                                                                        "field-class": "ma_fields.List",
                                                                        "validators": [],
                                                                        "imports": [],
                                                                    },
                                                                    "items": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.Nested",
                                                                            "schema-class": "nr_metadata.documents.services.records.schema.TitleItemSchema",
                                                                            "validators": [],
                                                                            "field": "i18n_strings",
                                                                            "imports": [],
                                                                        },
                                                                        "ui": {
                                                                            "marshmallow": {
                                                                                "field-class": "ma_fields.Nested",
                                                                                "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleItemUISchema",
                                                                                "field": "i18n_strings",
                                                                            }
                                                                        },
                                                                        "additionalProperties": {
                                                                            "type": "string"
                                                                        },
                                                                        "propertyNames": {
                                                                            "pattern": "^[a-z]{2}$"
                                                                        },
                                                                        "type": "object",
                                                                        "mapping": {
                                                                            "dynamic": True
                                                                        },
                                                                    },
                                                                    "ui": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.List"
                                                                        }
                                                                    },
                                                                    "type": "array",
                                                                },
                                                                "ancestors": {
                                                                    "marshmallow": {
                                                                        "field-class": "ma_fields.List",
                                                                        "validators": [],
                                                                        "imports": [],
                                                                    },
                                                                    "items": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.String",
                                                                            "validators": [],
                                                                            "imports": [],
                                                                        },
                                                                        "ui": {
                                                                            "marshmallow": {
                                                                                "field-class": "ma_fields.String"
                                                                            }
                                                                        },
                                                                        "type": "keyword",
                                                                    },
                                                                    "ui": {
                                                                        "marshmallow": {
                                                                            "field-class": "ma_fields.List"
                                                                        }
                                                                    },
                                                                    "type": "array",
                                                                },
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.Nested",
                                                                    "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                                    "generate": False,
                                                                }
                                                            },
                                                            "type": "object",
                                                        },
                                                        "@v": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "validators": [],
                                                                "field-name": "_version",
                                                                "imports": [],
                                                            },
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String",
                                                                    "field-name": "_version",
                                                                }
                                                            },
                                                            "type": "keyword",
                                                        },
                                                    },
                                                    "ui": {
                                                        "detail": "taxonomy_item",
                                                        "edit": "taxonomy_item",
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Nested",
                                                            "schema-class": "nr_metadata.common.services.records.ui_schema.NRAffiliationVocabularyUISchema",
                                                            "imports": [
                                                                {
                                                                    "import": "nr_metadata.common.services.records.ui_schema.NRAffiliationVocabularyUISchema"
                                                                }
                                                            ],
                                                        },
                                                    },
                                                    "pid-field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                                    "label.en": "Affiliation",
                                                    "sample": {
                                                        "skip": False,
                                                        "faker": "company",
                                                    },
                                                    "imports": [
                                                        {
                                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.relations.RelationsField"
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.relations.PIDRelation"
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.relations.InternalRelation"
                                                        },
                                                        {
                                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                                        },
                                                    ],
                                                    "model": "vocabularies",
                                                    "hint.cs": "Uveďte instituci/instituce, pod jejíž záštitou jste se na tvorbě objektu podíleli.",
                                                    "schema-prefix": "AffiliationsItem",
                                                    "name": "affiliations_item",
                                                    "relation-class": "PIDRelation",
                                                    "keys": [
                                                        {"target": "id", "key": "id"},
                                                        {
                                                            "target": "title",
                                                            "key": "title",
                                                        },
                                                        {
                                                            "target": "type",
                                                            "key": "type.id",
                                                        },
                                                        {
                                                            "model": {
                                                                "properties": {
                                                                    "parent": {
                                                                        "type": "keyword"
                                                                    },
                                                                    "level": {
                                                                        "type": "integer"
                                                                    },
                                                                    "title": {
                                                                        "items": {
                                                                            "ui": {
                                                                                "marshmallow": {
                                                                                    "field": "i18n_strings"
                                                                                }
                                                                            },
                                                                            "marshmallow": {
                                                                                "field": "i18n_strings"
                                                                            },
                                                                            "additionalProperties": {
                                                                                "type": "string"
                                                                            },
                                                                            "propertyNames": {
                                                                                "pattern": "^[a-z]{2}$"
                                                                            },
                                                                            "type": "object",
                                                                            "mapping": {
                                                                                "dynamic": True
                                                                            },
                                                                        },
                                                                        "type": "array",
                                                                    },
                                                                    "ancestors": {
                                                                        "items": {
                                                                            "type": "keyword"
                                                                        },
                                                                        "type": "array",
                                                                    },
                                                                },
                                                                "ui": {
                                                                    "marshmallow": {
                                                                        "schema-class": "oarepo_vocabularies.services.ui_schemas.HierarchyUISchema",
                                                                        "generate": False,
                                                                    }
                                                                },
                                                                "marshmallow": {
                                                                    "schema-class": "oarepo_vocabularies.services.schemas.HierarchySchema",
                                                                    "imports": [
                                                                        {
                                                                            "import": "oarepo_vocabularies.services.schemas.HierarchySchema"
                                                                        }
                                                                    ],
                                                                    "generate": False,
                                                                },
                                                                "type": "object",
                                                            },
                                                            "target": "hierarchy",
                                                            "key": "hierarchy",
                                                        },
                                                    ],
                                                    "model-class": "Vocabulary",
                                                    "relation-args": {
                                                        "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}, 'hierarchy']",
                                                        "pid_field": 'Vocabulary.pid.with_type_ctx("institutions")',
                                                    },
                                                    "type": "relation",
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.List"
                                                    }
                                                },
                                                "label.en": "Affiliation",
                                                "uniqueItems": True,
                                                "type": "array",
                                            },
                                            "nameType": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                    ],
                                                },
                                                "label.cs": "Typ",
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "l10n.LocalizedEnum",
                                                        "arguments": [
                                                            'value_prefix="nr_metadata.documents"'
                                                        ],
                                                    }
                                                },
                                                "label.en": "Type",
                                                "sample": [True, True],
                                                "hint.cs": "Jako tvůrce je možné označit osobu nebo instituci.",
                                                "enum": ["Organizational", "Personal"],
                                                "hint.en": "It is possible to designate a person or an institution as the creator/contributor.",
                                                "type": "keyword",
                                            },
                                            "fullName": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String"
                                                    }
                                                },
                                                "sample": {
                                                    "skip": False,
                                                    "faker": "name",
                                                },
                                                "type": "keyword",
                                                "required": True,
                                            },
                                            "authorityIdentifiers": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.List",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "items": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema",
                                                        "imports": [
                                                            {
                                                                "import": "nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema"
                                                            }
                                                        ],
                                                        "generate": False,
                                                        "validators": [],
                                                    },
                                                    "properties": {
                                                        "identifier": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "validators": [],
                                                                "imports": [],
                                                            },
                                                            "label.cs": "Identifikátor",
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "ma_fields.String"
                                                                }
                                                            },
                                                            "label.en": "Identifier",
                                                            "sample": {
                                                                "skip": False,
                                                                "faker": "isbn13",
                                                            },
                                                            "i18n.key": "identifier",
                                                            "type": "keyword",
                                                            "required": True,
                                                        },
                                                        "scheme": {
                                                            "marshmallow": {
                                                                "field-class": "ma_fields.String",
                                                                "validators": [],
                                                                "imports": [
                                                                    {
                                                                        "import": "oarepo_runtime.ui.marshmallow",
                                                                        "alias": "l10n",
                                                                    },
                                                                    {
                                                                        "import": "oarepo_runtime.ui.marshmallow",
                                                                        "alias": "l10n",
                                                                    },
                                                                ],
                                                            },
                                                            "label.cs": "Typ identifikátoru",
                                                            "ui": {
                                                                "marshmallow": {
                                                                    "field-class": "l10n.LocalizedEnum",
                                                                    "arguments": [
                                                                        'value_prefix="nr_metadata.documents"'
                                                                    ],
                                                                }
                                                            },
                                                            "label.en": "Identifier type",
                                                            "hint.cs": "Doporučujeme zadat alespoň jeden z typů identifikátorů.\nPokud potřebujete rozšířit nabídku typů identifikátorů, kontaktujte nás na support@narodni-repozitar.cz.\n",
                                                            "enum": [
                                                                "orcid",
                                                                "scopusID",
                                                                "researcherID",
                                                                "czenasAutID",
                                                                "vedidk",
                                                                "institutionalID",
                                                                "ISNI",
                                                                "ROR",
                                                                "ICO",
                                                                "DOI",
                                                            ],
                                                            "hint.en": "We recommend providing at least one of the identifier types.\nIf you need to expand the range of identifier types, contact us at support@narodni-repozitar.cz.\n",
                                                            "i18n.key": "identifier_type",
                                                            "type": "keyword",
                                                            "required": True,
                                                        },
                                                    },
                                                    "ui": {
                                                        "detail": "nr_authority_identifier",
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Nested",
                                                            "schema-class": "nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema",
                                                            "imports": [
                                                                {
                                                                    "import": "nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema"
                                                                }
                                                            ],
                                                            "generate": False,
                                                        },
                                                    },
                                                    "type": "object",
                                                },
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.List"
                                                    }
                                                },
                                                "uniqueItems": True,
                                                "type": "array",
                                            },
                                        },
                                        "ui": {
                                            "detail": "contributor",
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "nr_metadata.common.services.records.ui_schema.NRAuthorityUIUISchema",
                                                "imports": [
                                                    {
                                                        "import": "nr_metadata.common.services.records.ui_schema.NRAuthorityUIUISchema"
                                                    }
                                                ],
                                            },
                                        },
                                        "type": "object",
                                    },
                                    "ui": {
                                        "marshmallow": {"field-class": "ma_fields.List"}
                                    },
                                    "label.en": "Contributors",
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                                "itemPIDs": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.List",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.schema.identifiers.NRObjectIdentifierSchema",  # NOSONAR
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.schema.identifiers.NRObjectIdentifierSchema"
                                                }
                                            ],
                                            "generate": False,
                                            "validators": [],
                                        },
                                        "label.cs": "Identifikátor objektu",  # NOSONAR
                                        "properties": {
                                            "identifier": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [],
                                                },
                                                "label.cs": "Identifikátor objektu",
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String"
                                                    }
                                                },
                                                "label.en": "Object identifier",  # NOSONAR
                                                "sample": {
                                                    "skip": False,
                                                    "faker": "isbn13",
                                                },
                                                "type": "keyword",
                                                "required": True,
                                            },
                                            "scheme": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "validators": [],
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                        {
                                                            "import": "oarepo_runtime.ui.marshmallow",
                                                            "alias": "l10n",
                                                        },
                                                    ],
                                                },
                                                "label.cs": "Typ identifikátoru",
                                                "ui": {
                                                    "marshmallow": {
                                                        "field-class": "l10n.LocalizedEnum",
                                                        "arguments": [
                                                            'value_prefix="nr_metadata.documents"'
                                                        ],
                                                    }
                                                },
                                                "label.en": "Identifier type",
                                                "enum": [
                                                    "DOI",
                                                    "Handle",
                                                    "ISBN",
                                                    "ISSN",
                                                    "RIV",
                                                ],
                                                "type": "keyword",
                                                "required": True,
                                            },
                                        },
                                        "ui": {
                                            "detail": "nr_object_pid",
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "nr_metadata.ui_schema.identifiers.NRObjectIdentifierUISchema",  # NOSONAR
                                                "imports": [
                                                    {
                                                        "import": "nr_metadata.ui_schema.identifiers.NRObjectIdentifierUISchema"
                                                    }
                                                ],
                                                "generate": False,
                                            },
                                        },
                                        "label.en": "Object identifier",
                                        "type": "object",
                                    },
                                    "ui": {
                                        "marshmallow": {"field-class": "ma_fields.List"}
                                    },
                                    "uniqueItems": True,
                                    "type": "array",
                                },
                                "itemURL": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "URL",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "URL",
                                    "sample": {"skip": False, "faker": "url"},
                                    "type": "url",
                                },
                                "itemYear": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Integer",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Rok",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.Integer"
                                        }
                                    },
                                    "label.en": "Year",
                                    "type": "integer",
                                },
                                "itemVolume": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Ročník",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Volume",
                                    "type": "keyword",
                                },
                                "itemIssue": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Číslo",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Issue",
                                    "type": "keyword",
                                },
                                "itemStartPage": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Počáteční strana",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Start page",
                                    "type": "keyword",
                                },
                                "itemEndPage": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Poslední strana",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "End page",
                                    "type": "keyword",
                                },
                                "itemPublisher": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Vydavatel",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Publisher",
                                    "type": "keyword",
                                },
                                "itemRelationType": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.common.services.records.schema.NRItemRelationTypeVocabularySchema",
                                        "imports": [
                                            {
                                                "import": "nr_metadata.common.services.records.schema.NRItemRelationTypeVocabularySchema"
                                            }
                                        ],
                                        "validators": [],
                                    },
                                    "label.cs": "Typ vazby",
                                    "properties": {
                                        "id": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "sample": {"skip": True},
                                            "type": "keyword",
                                            "mapping": {
                                                "fields": {
                                                    "text": {
                                                        "type": "search_as_you_type"
                                                    }
                                                }
                                            },
                                        },
                                        "title": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                "imports": [
                                                    {
                                                        "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                    }
                                                ],
                                                "validators": [],
                                                "field": "i18n_strings",
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                        }
                                                    ],
                                                    "generate": False,
                                                    "field": "VocabularyI18nStrUIField()",
                                                }
                                            },
                                            "additionalProperties": {"type": "string"},
                                            "propertyNames": {"pattern": "^[a-z]{2}$"},
                                            "type": "object",
                                            "mapping": {
                                                "properties": {
                                                    "en": {"type": "search_as_you_type"}
                                                },
                                                "dynamic": True,
                                            },
                                        },
                                        "type": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                        "@v": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "validators": [],
                                                "field-name": "_version",
                                                "imports": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "field-name": "_version",
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                    },
                                    "description": "typ vztahu k původnímu popisovanému dok.",
                                    "ui": {
                                        "detail": "vocabulary_item",
                                        "edit": "vocabulary_item",
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.ui_schema.NRItemRelationTypeVocabularyUISchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.ui_schema.NRItemRelationTypeVocabularyUISchema"
                                                }
                                            ],
                                        },
                                    },
                                    "pid-field": 'Vocabulary.pid.with_type_ctx("item-relation-types")',
                                    "label.en": "Relation type",
                                    "imports": [
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.RelationsField"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.PIDRelation"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.InternalRelation"
                                        },
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                    ],
                                    "model": "vocabularies",
                                    "schema-prefix": "Itemrelationtype",
                                    "name": "itemRelationType",
                                    "relation-class": "PIDRelation",
                                    "keys": [
                                        {"target": "id", "key": "id"},
                                        {"target": "title", "key": "title"},
                                        {"target": "type", "key": "type.id"},
                                    ],
                                    "model-class": "Vocabulary",
                                    "relation-args": {
                                        "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                                        "pid_field": 'Vocabulary.pid.with_type_ctx("item-relation-types")',
                                    },
                                    "type": "relation",
                                },
                                "itemResourceType": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.common.services.records.schema.NRResourceTypeVocabularySchema",
                                        "imports": [
                                            {
                                                "import": "nr_metadata.common.services.records.schema.NRResourceTypeVocabularySchema"
                                            }
                                        ],
                                        "validators": [],
                                    },
                                    "label.cs": "Typ zdroje",
                                    "properties": {
                                        "id": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "sample": {"skip": True},
                                            "type": "keyword",
                                            "mapping": {
                                                "fields": {
                                                    "text": {
                                                        "type": "search_as_you_type"
                                                    }
                                                }
                                            },
                                        },
                                        "title": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                "imports": [
                                                    {
                                                        "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                    }
                                                ],
                                                "validators": [],
                                                "field": "i18n_strings",
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                        }
                                                    ],
                                                    "generate": False,
                                                    "field": "VocabularyI18nStrUIField()",
                                                }
                                            },
                                            "additionalProperties": {"type": "string"},
                                            "propertyNames": {"pattern": "^[a-z]{2}$"},
                                            "type": "object",
                                            "mapping": {
                                                "properties": {
                                                    "en": {"type": "search_as_you_type"}
                                                },
                                                "dynamic": True,
                                            },
                                        },
                                        "type": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                        "@v": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "validators": [],
                                                "field-name": "_version",
                                                "imports": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "field-name": "_version",
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                    },
                                    "ui": {
                                        "detail": "vocabulary_item",
                                        "edit": "vocabulary_item",
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.ui_schema.NRResourceTypeVocabularyUISchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.ui_schema.NRResourceTypeVocabularyUISchema"
                                                }
                                            ],
                                        },
                                    },
                                    "pid-field": 'Vocabulary.pid.with_type_ctx("resource-types")',
                                    "label.en": "Resource type",
                                    "sample": [True, True, True],
                                    "imports": [
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.RelationsField"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.PIDRelation"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.InternalRelation"
                                        },
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                    ],
                                    "model": "vocabularies",
                                    "schema-prefix": "Itemresourcetype",
                                    "name": "itemResourceType",
                                    "relation-class": "PIDRelation",
                                    "keys": [
                                        {"target": "id", "key": "id"},
                                        {"target": "title", "key": "title"},
                                        {"target": "type", "key": "type.id"},
                                    ],
                                    "model-class": "Vocabulary",
                                    "relation-args": {
                                        "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                                        "pid_field": 'Vocabulary.pid.with_type_ctx("resource-types")',
                                    },
                                    "type": "relation",
                                },
                            },
                            "description": "linkdata, propojení přidružených dokumentů a datasetů.",
                            "ui": {
                                "detail": "related_item",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRRelatedItemUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRRelatedItemUISchema"
                                        }
                                    ],
                                },
                            },
                            "label.en": "Link to/from other resources:",
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Link to/from other resources:",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "fundingReferences": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Projekt nebo financování",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRFundingReferenceSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRFundingReferenceSchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Projekt nebo financování",
                            "properties": {
                                "projectID": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Číslo projektu",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Project double",
                                    "type": "keyword",
                                    "required": True,
                                },
                                "projectName": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Název projektu",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Project name",
                                    "type": "fulltext",
                                },
                                "fundingProgram": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Výzkumný program",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Funding program",
                                    "type": "fulltext",
                                },
                                "funder": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.common.services.records.schema.NRFunderVocabularySchema",
                                        "imports": [
                                            {
                                                "import": "nr_metadata.common.services.records.schema.NRFunderVocabularySchema"
                                            }
                                        ],
                                        "validators": [],
                                    },
                                    "label.cs": "Poskytovatel financí",
                                    "properties": {
                                        "id": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "sample": {"skip": True},
                                            "type": "keyword",
                                            "mapping": {
                                                "fields": {
                                                    "text": {
                                                        "type": "search_as_you_type"
                                                    }
                                                }
                                            },
                                        },
                                        "title": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                "imports": [
                                                    {
                                                        "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                    }
                                                ],
                                                "validators": [],
                                                "field": "i18n_strings",
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                    "imports": [
                                                        {
                                                            "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                        }
                                                    ],
                                                    "generate": False,
                                                    "field": "VocabularyI18nStrUIField()",
                                                }
                                            },
                                            "additionalProperties": {"type": "string"},
                                            "propertyNames": {"pattern": "^[a-z]{2}$"},
                                            "type": "object",
                                            "mapping": {
                                                "properties": {
                                                    "en": {"type": "search_as_you_type"}
                                                },
                                                "dynamic": True,
                                            },
                                        },
                                        "type": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "imports": [],
                                                "validators": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "imports": [],
                                                    "validators": [],
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                        "@v": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "validators": [],
                                                "field-name": "_version",
                                                "imports": [],
                                            },
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String",
                                                    "field-name": "_version",
                                                }
                                            },
                                            "type": "keyword",
                                        },
                                    },
                                    "ui": {
                                        "detail": "vocabulary_item",
                                        "edit": "vocabulary_item",
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.ui_schema.NRFunderVocabularyUISchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.ui_schema.NRFunderVocabularyUISchema"
                                                }
                                            ],
                                        },
                                    },
                                    "pid-field": 'Vocabulary.pid.with_type_ctx("funders")',
                                    "label.en": "Funder",
                                    "imports": [
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.RelationsField"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.PIDRelation"
                                        },
                                        {
                                            "import": "oarepo_runtime.relations.InternalRelation"
                                        },
                                        {
                                            "import": "invenio_vocabularies.records.api.Vocabulary"
                                        },
                                    ],
                                    "model": "vocabularies",
                                    "schema-prefix": "Funder",
                                    "name": "funder",
                                    "relation-class": "PIDRelation",
                                    "keys": [
                                        {"target": "id", "key": "id"},
                                        {"target": "title", "key": "title"},
                                        {"target": "type", "key": "type.id"},
                                    ],
                                    "model-class": "Vocabulary",
                                    "relation-args": {
                                        "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                                        "pid_field": 'Vocabulary.pid.with_type_ctx("funders")',
                                    },
                                    "type": "relation",
                                },
                            },
                            "ui": {
                                "detail": "funding_reference",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRFundingReferenceUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRFundingReferenceUISchema"
                                        }
                                    ],
                                },
                            },
                            "label.en": "Funding",
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Funding",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "version": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Verze zdroje",
                        "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                        "label.en": "Resource version",
                        "sample": [True, True, True, True, True],
                        "type": "keyword",
                    },
                    "geoLocations": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Geolokace",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRGeoLocationSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRGeoLocationSchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Geolokace",
                            "properties": {
                                "geoLocationPlace": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "description": "Free description of the location; ie. Atlantic Ocean",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "keyword",
                                    "required": True,
                                },
                                "geoLocationPoint": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.common.services.records.schema.NRGeoLocationPointSchema",
                                        "imports": [
                                            {
                                                "import": "nr_metadata.common.services.records.schema.NRGeoLocationPointSchema"
                                            }
                                        ],
                                        "validators": [],
                                    },
                                    "properties": {
                                        "pointLongitude": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Float",  # NOSONAR
                                                "validators": [
                                                    "ma_validate.Range(min_inclusive=-180.0, max_inclusive=180.0)"
                                                ],
                                                "imports": [],
                                            },
                                            "label.cs": "Zeměpisná délka",
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Float"
                                                }
                                            },
                                            "label.en": "Longitude",
                                            "minimum": -180.0,
                                            "maximum": 180.0,
                                            "type": "double",
                                            "required": True,
                                        },
                                        "pointLatitude": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Float",
                                                "validators": [
                                                    "ma_validate.Range(min_inclusive=-90.0, max_inclusive=90.0)"
                                                ],
                                                "imports": [],
                                            },
                                            "label.cs": "Zeměpisná šířka",
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Float"
                                                }
                                            },
                                            "label.en": "Latitude",
                                            "minimum": -90.0,
                                            "maximum": 90.0,
                                            "type": "double",
                                            "required": True,
                                        },
                                    },
                                    "ui": {
                                        "detail": "geolocation_point",
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.ui_schema.NRGeoLocationPointUISchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.ui_schema.NRGeoLocationPointUISchema"
                                                }
                                            ],
                                        },
                                    },
                                    "type": "object",
                                },
                            },
                            "ui": {
                                "detail": "geolocation",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRGeoLocationUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRGeoLocationUISchema"
                                        }
                                    ],
                                },
                            },
                            "label.en": "Geolocation",
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Geolocation",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "accessibility": {
                        "marshmallow": {
                            "field-class": "MultilingualField",
                            "imports": [
                                {
                                    "import": "oarepo_runtime.i18n.schema.MultilingualField"
                                }
                            ],
                            "validators": [],
                        },
                        "label.cs": "Dostupnost zdroje",
                        "items": {
                            "marshmallow": {
                                "field-class": "I18nStrField",
                                "schema-class": None,
                                "imports": [
                                    {
                                        "import": "oarepo_runtime.i18n.schema.I18nStrField"
                                    }
                                ],
                                "generate": False,
                                "validators": [],
                            },
                            "properties": {
                                "lang": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "keyword",
                                },
                                "value": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "type": "fulltext+keyword",
                                },
                            },
                            "ui": {
                                "detail": "multilingual",
                                "marshmallow": {
                                    "field-class": "I18nStrUIField",
                                    "schema-class": None,
                                    "imports": [
                                        {
                                            "import": "oarepo_runtime.i18n.ui_schema.I18nStrUIField"
                                        }
                                    ],
                                },
                            },
                            "sample": {"skip": False},
                            "type": "i18nStr",
                        },
                        "ui": {
                            "detail": "string",
                            "marshmallow": {
                                "field-class": "MultilingualLocalizedUIField",
                                "imports": [
                                    {
                                        "import": "oarepo_runtime.i18n.ui_schema.MultilingualLocalizedUIField"
                                    },
                                    {
                                        "import": "oarepo_runtime.i18n.ui_schema.MultilingualUIField"
                                    },
                                ],
                            },
                        },
                        "label.en": "Resource accessibility",
                        "type": "array",
                    },
                    "series": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Série",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NRSeriesSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NRSeriesSchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Série",
                            "properties": {
                                "seriesTitle": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Název edice",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Series title",
                                    "sample": [True, True, True],
                                    "type": "keyword",
                                    "required": True,
                                },
                                "seriesVolume": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Svazek edice",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Series volume",
                                    "sample": [True, True, True, True],
                                    "type": "keyword",
                                },
                            },
                            "ui": {
                                "detail": "series",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRSeriesUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NRSeriesUISchema"
                                        }
                                    ],
                                },
                            },
                            "label.en": "Series",
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Series",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "externalLocation": {
                        "marshmallow": {
                            "field-class": "ma_fields.Nested",
                            "schema-class": "nr_metadata.common.services.records.schema.NRExternalLocationSchema",
                            "imports": [
                                {
                                    "import": "nr_metadata.common.services.records.schema.NRExternalLocationSchema"
                                }
                            ],
                            "validators": [],
                        },
                        "label.cs": "Externí umístění",
                        "properties": {
                            "externalLocationURL": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",
                                    "validators": [],
                                    "imports": [],
                                },
                                "label.cs": "Externí umístění zdroje",
                                "ui": {
                                    "marshmallow": {"field-class": "ma_fields.String"}
                                },
                                "label.en": "Resource external location",
                                "sample": {"skip": False, "faker": "url"},
                                "type": "url",
                                "required": True,
                            },
                            "externalLocationNote": {
                                "marshmallow": {
                                    "field-class": "ma_fields.String",
                                    "validators": [],
                                    "imports": [],
                                },
                                "label.cs": "Poznámka",
                                "ui": {
                                    "marshmallow": {"field-class": "ma_fields.String"}
                                },
                                "label.en": "Note",
                                "type": "fulltext",
                            },
                        },
                        "ui": {
                            "detail": "external_location",
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.ui_schema.NRExternalLocationUISchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.ui_schema.NRExternalLocationUISchema"
                                    }
                                ],
                            },
                        },
                        "label.en": "External location",
                        "type": "object",
                    },
                    "originalRecord": {
                        "marshmallow": {
                            "field-class": "ma_fields.String",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Odkaz na původní záznam",
                        "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                        "label.en": "Original record URL",
                        "sample": {"skip": False, "faker": "url"},
                        "type": "url",
                    },
                    "objectIdentifiers": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Identifikátory objektu",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.schema.identifiers.NRObjectIdentifierSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.schema.identifiers.NRObjectIdentifierSchema"
                                    }
                                ],
                                "generate": False,
                                "validators": [],
                            },
                            "label.cs": "Identifikátor objektu",
                            "properties": {
                                "identifier": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Identifikátor objektu",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Object identifier",
                                    "sample": {"skip": False, "faker": "isbn13"},
                                    "type": "keyword",
                                    "required": True,
                                },
                                "scheme": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                        ],
                                    },
                                    "label.cs": "Typ identifikátoru",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "l10n.LocalizedEnum",
                                            "arguments": [
                                                'value_prefix="nr_metadata.documents"'
                                            ],
                                        }
                                    },
                                    "label.en": "Identifier type",
                                    "enum": ["DOI", "Handle", "ISBN", "ISSN", "RIV"],
                                    "type": "keyword",
                                    "required": True,
                                },
                            },
                            "ui": {
                                "detail": "nr_object_pid",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.ui_schema.identifiers.NRObjectIdentifierUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.ui_schema.identifiers.NRObjectIdentifierUISchema"
                                        }
                                    ],
                                    "generate": False,
                                },
                            },
                            "label.en": "Object identifier",
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Object identifiers",
                        "uniqueItems": True,
                        "type": "array",
                    },
                    "systemIdentifiers": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Systémové identifikátory",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.schema.identifiers.NRSystemIdentifierSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.schema.identifiers.NRSystemIdentifierSchema"
                                    }
                                ],
                                "generate": False,
                                "validators": [],
                            },
                            "label.cs": "Systémový identifikátor",
                            "properties": {
                                "identifier": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Systémový identifikátor",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "System Identifier",
                                    "type": "keyword",
                                    "required": True,
                                },
                                "scheme": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                        ],
                                    },
                                    "label.cs": "Typ identifikátoru",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "l10n.LocalizedEnum",
                                            "arguments": [
                                                'value_prefix="nr_metadata.documents"'
                                            ],
                                        }
                                    },
                                    "label.en": "Identifier type",
                                    "enum": [
                                        "nusl",
                                        "nuslOAI",
                                        "originalRecordOAI",
                                        "catalogueSysNo",
                                        "nrOAI",
                                    ],
                                    "type": "keyword",
                                    "required": True,
                                },
                            },
                            "ui": {
                                "detail": "identifier",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.ui_schema.identifiers.NRSystemIdentifierUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.ui_schema.identifiers.NRSystemIdentifierUISchema"
                                        }
                                    ],
                                    "generate": False,
                                },
                            },
                            "label.en": "System identifier",
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "System identifiers",
                        "type": "array",
                    },
                    "events": {
                        "marshmallow": {
                            "field-class": "ma_fields.List",
                            "validators": [],
                            "imports": [],
                        },
                        "label.cs": "Události",
                        "items": {
                            "marshmallow": {
                                "field-class": "ma_fields.Nested",
                                "schema-class": "nr_metadata.common.services.records.schema.NREventSchema",
                                "imports": [
                                    {
                                        "import": "nr_metadata.common.services.records.schema.NREventSchema"
                                    }
                                ],
                                "validators": [],
                            },
                            "label.cs": "Událost",
                            "properties": {
                                "eventNameOriginal": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "label.cs": "Název akce",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String"
                                        }
                                    },
                                    "label.en": "Event name",
                                    "type": "fulltext",
                                    "required": True,
                                },
                                "eventNameAlternate": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.List",
                                        "validators": [],
                                        "imports": [],
                                    },
                                    "items": {
                                        "marshmallow": {
                                            "field-class": "ma_fields.String",
                                            "validators": [],
                                            "imports": [],
                                        },
                                        "label.cs": "Alternativní název akce",
                                        "ui": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String"
                                            }
                                        },
                                        "label.en": "Event alternate name",
                                        "type": "fulltext",
                                    },
                                    "ui": {
                                        "marshmallow": {"field-class": "ma_fields.List"}
                                    },
                                    "type": "array",
                                },
                                "eventDate": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.String",
                                        "validators": [
                                            "mu_fields_edtf.EDTFValidator(types=(EDTFInterval,))"
                                        ],
                                        "imports": [
                                            {
                                                "import": "edtf.Interval",
                                                "alias": "EDTFInterval",
                                            },
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                            {
                                                "import": "marshmallow_utils.fields.edtfdatestring",
                                                "alias": "mu_fields_edtf",
                                            },
                                            {
                                                "import": "edtf.Interval",
                                                "alias": "EDTFInterval",
                                            },
                                            {
                                                "import": "oarepo_runtime.ui.marshmallow",
                                                "alias": "l10n",
                                            },
                                            {
                                                "import": "marshmallow_utils.fields.edtfdatestring",
                                                "alias": "mu_fields_edtf",
                                            },
                                        ],
                                    },
                                    "label.cs": "Datum konání akce",
                                    "ui": {
                                        "marshmallow": {
                                            "field-class": "l10n.LocalizedEDTFInterval"
                                        }
                                    },
                                    "label.en": "Event date",
                                    "type": "edtf-interval",
                                    "required": True,
                                },
                                "eventLocation": {
                                    "marshmallow": {
                                        "field-class": "ma_fields.Nested",
                                        "schema-class": "nr_metadata.common.services.records.schema.NRLocationSchema",
                                        "imports": [
                                            {
                                                "import": "nr_metadata.common.services.records.schema.NRLocationSchema"
                                            }
                                        ],
                                        "validators": [],
                                    },
                                    "label.cs": "Umístění",
                                    "properties": {
                                        "place": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.String",
                                                "validators": [],
                                                "imports": [],
                                            },
                                            "label.cs": "Místo",
                                            "ui": {
                                                "marshmallow": {
                                                    "field-class": "ma_fields.String"
                                                }
                                            },
                                            "label.en": "Place",
                                            "type": "keyword",
                                            "required": True,
                                        },
                                        "country": {
                                            "marshmallow": {
                                                "field-class": "ma_fields.Nested",
                                                "schema-class": "nr_metadata.common.services.records.schema.NRCountryVocabularySchema",
                                                "imports": [
                                                    {
                                                        "import": "nr_metadata.common.services.records.schema.NRCountryVocabularySchema"
                                                    }
                                                ],
                                                "validators": [],
                                            },
                                            "label.cs": "Země",
                                            "properties": {
                                                "id": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "imports": [],
                                                        "validators": [],
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "imports": [],
                                                            "validators": [],
                                                        }
                                                    },
                                                    "sample": {"skip": True},
                                                    "type": "keyword",
                                                    "mapping": {
                                                        "fields": {
                                                            "text": {
                                                                "type": "search_as_you_type"
                                                            }
                                                        }
                                                    },
                                                },
                                                "title": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.Nested",
                                                        "schema-class": "invenio_vocabularies.services.records.schema.TitleSchema",
                                                        "imports": [
                                                            {
                                                                "import": "invenio_vocabularies.services.schema.i18n_strings"
                                                            }
                                                        ],
                                                        "validators": [],
                                                        "field": "i18n_strings",
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.Nested",
                                                            "schema-class": "nr_metadata.documents.services.records.ui_schema.TitleUISchema",
                                                            "imports": [
                                                                {
                                                                    "import": "oarepo_vocabularies.services.ui_schemas.VocabularyI18nStrUIField"
                                                                }
                                                            ],
                                                            "generate": False,
                                                            "field": "VocabularyI18nStrUIField()",
                                                        }
                                                    },
                                                    "additionalProperties": {
                                                        "type": "string"
                                                    },
                                                    "propertyNames": {
                                                        "pattern": "^[a-z]{2}$"
                                                    },
                                                    "type": "object",
                                                    "mapping": {
                                                        "properties": {
                                                            "en": {
                                                                "type": "search_as_you_type"
                                                            }
                                                        },
                                                        "dynamic": True,
                                                    },
                                                },
                                                "type": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "imports": [],
                                                        "validators": [],
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "imports": [],
                                                            "validators": [],
                                                        }
                                                    },
                                                    "type": "keyword",
                                                },
                                                "@v": {
                                                    "marshmallow": {
                                                        "field-class": "ma_fields.String",
                                                        "validators": [],
                                                        "field-name": "_version",
                                                        "imports": [],
                                                    },
                                                    "ui": {
                                                        "marshmallow": {
                                                            "field-class": "ma_fields.String",
                                                            "field-name": "_version",
                                                        }
                                                    },
                                                    "type": "keyword",
                                                },
                                            },
                                            "ui": {
                                                "detail": "vocabulary_item",
                                                "edit": "vocabulary_item",
                                                "marshmallow": {
                                                    "field-class": "ma_fields.Nested",
                                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NRCountryVocabularyUISchema",
                                                    "imports": [
                                                        {
                                                            "import": "nr_metadata.common.services.records.ui_schema.NRCountryVocabularyUISchema"
                                                        }
                                                    ],
                                                },
                                            },
                                            "pid-field": 'Vocabulary.pid.with_type_ctx("countries")',
                                            "label.en": "Country",
                                            "imports": [
                                                {
                                                    "import": "invenio_vocabularies.records.api.Vocabulary"
                                                },
                                                {
                                                    "import": "oarepo_runtime.relations.RelationsField"
                                                },
                                                {
                                                    "import": "oarepo_runtime.relations.PIDRelation"
                                                },
                                                {
                                                    "import": "oarepo_runtime.relations.InternalRelation"
                                                },
                                                {
                                                    "import": "invenio_vocabularies.records.api.Vocabulary"
                                                },
                                            ],
                                            "model": "vocabularies",
                                            "schema-prefix": "Country",
                                            "name": "country",
                                            "relation-class": "PIDRelation",
                                            "keys": [
                                                {"target": "id", "key": "id"},
                                                {"target": "title", "key": "title"},
                                                {"target": "type", "key": "type.id"},
                                            ],
                                            "model-class": "Vocabulary",
                                            "relation-args": {
                                                "keys": "['id', 'title', {'key': 'type.id', 'target': 'type'}]",
                                                "pid_field": 'Vocabulary.pid.with_type_ctx("countries")',
                                            },
                                            "type": "relation",
                                        },
                                    },
                                    "ui": {
                                        "detail": "location",
                                        "marshmallow": {
                                            "field-class": "ma_fields.Nested",
                                            "schema-class": "nr_metadata.common.services.records.ui_schema.NRLocationUISchema",
                                            "imports": [
                                                {
                                                    "import": "nr_metadata.common.services.records.ui_schema.NRLocationUISchema"
                                                }
                                            ],
                                        },
                                    },
                                    "label.en": "Location",
                                    "type": "object",
                                    "required": True,
                                },
                            },
                            "ui": {
                                "detail": "identifier",
                                "marshmallow": {
                                    "field-class": "ma_fields.Nested",
                                    "schema-class": "nr_metadata.common.services.records.ui_schema.NREventUISchema",
                                    "imports": [
                                        {
                                            "import": "nr_metadata.common.services.records.ui_schema.NREventUISchema"
                                        }
                                    ],
                                },
                            },
                            "label.en": "Event",
                            "type": "object",
                        },
                        "ui": {"marshmallow": {"field-class": "ma_fields.List"}},
                        "label.en": "Events",
                        "type": "array",
                    },
                },
                "ui": {
                    "marshmallow": {
                        "base-classes": ["ma.Schema"],
                        "field-class": "ma_fields.Nested",
                        "schema-class": "nr_metadata.documents.services.records.ui_schema.NRDocumentMetadataUISchema",
                        "generate": True,
                    }
                },
                "type": "object",
            },
            "id": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "write": False,
                    "read": False,
                    "validators": [],
                    "imports": [],
                },
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "facets": {"searchable": True},
                "sample": {"skip": True},
                "type": "keyword",
            },
            "created": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "write": False,
                    "read": False,
                    "validators": ["validate_datetime"],
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_datetime"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                        {"import": "oarepo_runtime.validation.validate_datetime"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                    ],
                },
                "ui": {"marshmallow": {"field-class": "l10n.LocalizedDateTime"}},
                "facets": {"searchable": True},
                "sample": {"skip": True},
                "type": "datetime",
            },
            "updated": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "write": False,
                    "read": False,
                    "validators": ["validate_datetime"],
                    "imports": [
                        {"import": "oarepo_runtime.validation.validate_datetime"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                        {"import": "oarepo_runtime.validation.validate_datetime"},
                        {"import": "oarepo_runtime.ui.marshmallow", "alias": "l10n"},
                    ],
                },
                "ui": {"marshmallow": {"field-class": "l10n.LocalizedDateTime"}},
                "facets": {"searchable": True},
                "sample": {"skip": True},
                "type": "datetime",
            },
            "$schema": {
                "marshmallow": {
                    "field-class": "ma_fields.String",
                    "write": False,
                    "read": False,
                    "validators": [],
                    "imports": [],
                },
                "ui": {"marshmallow": {"field-class": "ma_fields.String"}},
                "facets": {"searchable": True},
                "sample": {"skip": True},
                "type": "keyword",
            },
        },
        "record-service-bases": ["invenio_records_resources.services.RecordService"],
        "package-base-upper": "DOCUMENTS",
        "record-ui-serializer-class": "nr_metadata.documents.resources.records.ui.DocumentsUIJSONSerializer",
        "extension-suffix": "documents",
        "record-api-blueprints-setup-cfg": "documents",
        "schema-file": "nr_metadata/documents/records/jsonschemas/documents-1.0.0.json",
        "config-package": "nr_metadata.documents.config",
        "ui": {
            "marshmallow": {
                "base-classes": ["InvenioUISchema"],
                "schema-class": "nr_metadata.documents.services.records.ui_schema.NRDocumentRecordUISchema",
                "imports": [
                    {
                        "import": "nr_metadata.documents.services.records.ui_schema.NRDocumentRecordUISchema"
                    }
                ],
                "generate": True,
            }
        },
        "proxies-current-service": "nr_metadata.documents.proxies.current_service",
        "schema-version": "1.0.0",
        "permissions": {"presets": []},
        "record-metadata-bases": ["invenio_records.models.RecordMetadataBase"],
        "invenio-record-resource-extra-code": "",
        "record-resource-class": "nr_metadata.documents.resources.records.resource.DocumentsResource",
        "invenio-record-permissions-extra-code": "",
        "record-records-package": "nr_metadata.documents.records",
        "marshmallow": {
            "base-classes": ["InvenioBaseRecordSchema"],
            "schema-class": "nr_metadata.documents.services.records.schema.NRDocumentRecordSchema",
            "imports": [
                {
                    "import": "nr_metadata.documents.services.records.schema.NRDocumentRecordSchema"
                }
            ],
            "generate": True,
        },
        "record-prefix": "Documents",
        "service-id": "documents",
        "index-name": "documents-documents-1.0.0",
        "ui-layout": "nr_metadata/documents/models/ui.json",
        "invenio-record-service-config-extra-code": "",
        "saved-model-file": "nr_metadata/documents/models/model.json",
        "config-resource-config-key": "DOCUMENTS_RESOURCE_CONFIG_DOCUMENTS",
        "multilingual-schema-class": "nr_metadata.documents.services.records.multilingual_schema.MultilingualSchema",
        "model-name": "documents",
        "package-base": "documents",
        "record-ui-schema-class": "nr_metadata.documents.services.records.ui_schema.DocumentsUISchema",
        "record-mapping-setup-cfg": "documents",
        "translations-setup-cfg": "nr_metadata.documents",
        "invenio-record-service-extra-code": "",
        "package-path": "nr_metadata/documents",
        "record-service-config-class": "nr_metadata.documents.services.records.config.DocumentsServiceConfig",
        "invenio-record-resource-config-extra-code": "",
        "flask-extension-name": "documents",
        "record-resource-config-class": "nr_metadata.documents.resources.records.config.DocumentsResourceConfig",
        "record-ui-schema-metadata-class": "nr_metadata.documents.services.records.ui_schema.DocumentsMetadataUISchema",
        "script-import-sample-data": "data/sample_data.yaml",
        "generate-record-pid-field": True,
        "record-search-options-class": "nr_metadata.documents.services.records.search.DocumentsSearchOptions",
        "invenio-proxies-extra-code": "",
        "pid-field-cls": "PIDField",
        "record-resource-blueprint-name": "Documents",
        "ext-class": "nr_metadata.documents.ext.DocumentsExt",
        "invenio-version-extra-code": "",
        "multilingual-ui-schema-class": "nr_metadata.documents.services.records.multilingual_schema.MultilingualUISchema",
        "invenio-record-metadata-extra-code": "",
        "mapping-file": "nr_metadata/documents/records/mappings/os-v2/documents/documents-1.0.0.json",
        "i18n-schema-class": "nr_metadata.documents.services.records.i18nStr_schema.i18nStrSchema",
        "record-service-class": "nr_metadata.documents.services.records.service.DocumentsService",
        "record-resource-config-bases": [
            "invenio_records_resources.resources.RecordResourceConfig"
        ],
        "invenio-views-extra-code": "",
        "record-schema-class": "nr_metadata.documents.services.records.schema.DocumentsSchema",
        "invenio-record-facets-extra-code": "",
        "record-service-config-bases": [
            "invenio_records_resources.services.RecordServiceConfig"
        ],
        "config-resource-register-blueprint-key": "DOCUMENTS_REGISTER_BLUEPRINT",
        "config-resource-class-key": "DOCUMENTS_RESOURCE_CLASS_DOCUMENTS",
        "multilingual-dumper-class": "nr_metadata.documents.records.multilingual_dumper.MultilingualDumper",
        "i18n-ui-schema-class": "nr_metadata.documents.services.records.i18nStr_schema.i18nStrUISchema",
        "config-dummy-class": "nr_metadata.documents.config.DummyClass",
        "oarepo-models-setup-cfg": "documents",
        "invenio-record-extra-code": "",
        "record-resources-package": "nr_metadata.documents.resources.records",
        "package": "nr_metadata.documents",
        "create-blueprint-from-app": "nr_metadata.documents.views.create_blueprint_from_app_documents",
        "proxies-current-resource": "nr_metadata.documents.proxies.current_resource",
        "config-service-config-key": "DOCUMENTS_SERVICE_CONFIG_DOCUMENTS",
        "record-facets-class": "nr_metadata.documents.services.records.facets.Test",
        "pid-field-args": ["create=True"],
        "invenio-config-extra-code": "",
        "invenio-record-search-options-extra-code": "",
        "record-class": "nr_metadata.documents.records.api.DocumentsRecord",
        "record-metadata-class": "nr_metadata.documents.records.models.DocumentsMetadata",
        "record-schema-metadata-alembic": "documents",
        "kebap-package": "nr-metadata.documents",
        "record-services-package": "nr_metadata.documents.services.records",
        "record-dumper-extensions": [],
        "invenio-record-schema-extra-code": "",
        "collection-url": "/nr-metadata.documents/",
        "record-schema-metadata-setup-cfg": "documents",
        "pid-field-context": "PIDFieldContext",
        "record-jsonschemas-setup-cfg": "documents",
        "invenio-record-dumper-extra-code": "",
        "pid-field-imports": [
            {"import": "invenio_records_resources.records.systemfields.pid.PIDField"},
            {
                "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
            },
            {"import": "invenio_pidstore.providers.recordid_v2.RecordIdProviderV2"},
        ],
        "record-prefix-snake": "documents",
        "profile-package": "records",
        "invenio-record-object-schema-extra-code": "",
        "pid-field-provider": "RecordIdProviderV2",
        "schema-server": "local://",
        "record-metadata-table-name": "documents_metadata",
        "record-resource-bases": ["invenio_records_resources.resources.RecordResource"],
        "flask-commands-setup-cfg": "documents",
        "plugins": {
            "builder": {
                "disable": [
                    "script_sample_data",
                    "invenio_cli_setup_cfg",
                    "invenio_ext_setup_cfg",
                    "invenio_record_jsonschemas_setup_cfg",
                    "invenio_record_metadata_alembic_setup_cfg",
                    "invenio_record_metadata_models_setup_cfg",
                    "invenio_record_resource_setup_cfg",
                    "invenio_record_search_setup_cfg",
                ]
            }
        },
        "record-blueprints-setup-cfg": "documents",
        "record-schema-metadata-class": "nr_metadata.documents.services.records.schema.DocumentsMetadataSchema",
        "record-bases": ["invenio_records_resources.records.api.Record"],
        "record-service-config-generate-links": True,
        "jsonschemas-package": "nr_metadata.documents.records.jsonschemas",
        "config-service-class-key": "DOCUMENTS_SERVICE_CLASS_DOCUMENTS",
        "record-dumper-class": "nr_metadata.documents.records.dumper.DocumentsDumper",
        "record-permissions-class": "nr_metadata.documents.services.records.permissions.DocumentsPermissionPolicy",
        "mapping-package": "nr_metadata.documents.records.mappings",
        "schema-name": "documents-1.0.0.json",
        "invenio-ext-extra-code": "",
    }
}
