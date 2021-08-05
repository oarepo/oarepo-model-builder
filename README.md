# OARepo model builder

An utility library that generates OARepo required data model files from a JSON specification file.

## Installation

```shell
poetry install oarepo-model-builder
```

## Data model specification file

Data model specification should be a JSON5 formatted file based on JSON Schema with the following OArepo specific
extension keywords:

### oarepo:use

- Defines a reference to another datamodel. Contents of referenced datamodel will be used in place of this directive.
- Can be used anywhere in the specification file.
- This directive will be replaced by a referred datamodel type contents.
- Only new properties will be added to current property/object.
- All referenced datamodels must be registered under *datamodel* entrypoints (see **Entrypoints**)

#### Syntax

```json
"oarepo:use": List[string] | string   // list of datamodel type references or single string reference 
```

#### Example Usage:

The following source specification:

```json5
// datamodel.json5
{
  "title": "Test record v1.0.0",
  "type": "object",
  "additionalProperties": false,
  "oarepo:use": [
    "include1"
  ],
  "properties": {
    "field0": {
      "oarepo:use": "include2"
    }
  }
}
```

```json5
// datamodels/include1.json5
{
  "title": "Included properties v1.0.0",
  "type": "object",
  "additionalProperties": true,
  "properties": {
    "includedField1": {
      "type": "string",
    }
  }
}
```

```json5
// datamodels/include2.json5
{
  "type": "number"
}
```

```python
# setup.py
entry_points = {
    'oarepo_model_builder.datamodels': [
        'includes = mypkg.datamodels'
    ],
    ...
}
```

Will be compiled into resulting JSON Schema:

```json
{
  "title": "Test record v1.0.0",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "field0": {
      "type": "number"
    },
    "includedField1": {
      "type": "string"
    }
  }
}
```

### oarepo:search

- Specifies how the current field/object should be indexed and handled for search, filtering and aggregations
- Used by the ElasticSearch Mapping generator to generate property mappings.
- If not present on a property, a default mapping type of **keyword** or **object** (for object-type properties) is assumed in resulting mapping output
- Value can be either string or object.
- This directive is omitted from the JSON Schema builder output

#### Syntax

```json5

mapping_config: string  // string value represents an ES mapping type of property
// or
mapping_config: object  // you can also pass object for more complex property mapping configurations
// or
mapping_config: false  // parent field should be omitted from the generated ES mapping output

"oarepo:search": {
  "mapping": mapping_config  // "oarepo:search" block will be substituted by mapping_object configuration ES mapping output
}
// or
"oarepo:search": string | false  // "string" represents an ES mapping type of the parent property
```

#### Example usage

The following source specification:

```json5
{
  "properties": {
    "testNoMapping": {
      "type": "string",
      "oarepo:search": false
    },
    "testDefault": {
      "type": "string"
    },
    "testExplicit": {
      "type": "string",
      "oarepo:search": {
        "mapping": "text"
      }
    },
    "testShorthand": {
      "type": "string",
      "oarepo:search": "date"
    },
    "testObject": {
      "type": "string",
      "oarepo:search": {
        "mapping": {
          "type": "text",
          "index": "false"
        }
      }
    },
    "testArray": {
      "type": "array",
      "items": {
        "type": "string",
        "oarepo:search": "date"
      }
    }
  }
}
```

Will result in the following files:

```json5
// mappings/v7/mymodel-v1.0.0.json
{
  "mappings": {
    "properties": {
      "testDefault": {"type": "keyword"},
      "testExplicit": {"type": "text"},
      "testShorthand": {"type": "date"},
      "testObject": {
        "type": "text",
        "index": "false"
      },
      "testArray": {"type": "date"}
    }
  }
}
```

```json5
// jsonschemas/.../mymodel-v1.0.0.json
{
  "properties": {
    "testNoMapping": {"type": "string"},
    "testDefault": {"type": "string"},
    "testExplicit": {"type": "string"},
    "testShorthand": {"type": "string"},
    "testObject": {"type": "string"},
    "testArray": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

### oarepo:ui

- Directive used to specify a field metadata to be used by UI representations of the data model

#### Syntax

```json5
multilingual_string: {lang_code: value, ...}

"oarepo:ui": {
  "title": multilingual_string,   // Property or object title
  "label": multilingual_string,   // Label to be displayed on property input fields
  "hint": multilingual_string     // Additional hint to be displayed on property input fields 
}
```

### Example usage

The following source specification:
```json5

{
  "title": "Test record v1.0.0",
  "type": "object",
  "oarepo:ui":  {
    "title": {
      "cs": "Testovaci zaznam",
      "en": "Test record"
    },
  },
  "properties": {
    "field1": {
      "type": "string",
      "oarepo:ui": {
        "label": {
          "en": "Test field 1"
        },
        "hint": {
          "cs": "Vyplnte testovaci field",
          "en": "Please provide test field input"
        }
      }
    }
  }
}
```

Will result in the following files:

##### TODO(@mesemus):

## Customization

### Build configuration

You can override some build process defaults using a custom JSON configuration file, starting with configuration
from `./config/defauts.json`.
```json5
// build-config.json
{
  "jsonschema": {
    "type": "object",
    "additionalProperties": false
  },
  "search": {
    "default_mapping_type": "keyword",
    "mapping": {
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
        "dynamic": false,
        "date_detection": false,
        "numeric_detection": false,
        "properties": {}
      }
    }
  }
}
```

### Entrypoints

This package uses the following entrypoints in the build process to determine, which builders and data models
should be considered:

#### oarepo_model_builder.source
Classes responsible for parsing the whole source data model specification file.

Default:
```python
datamodel = "oarepo_model_builder.handlers:DataModelBuilder"
```

#### oarepo_model_builder.elements
Classes for building the output files from elements in a source data model specification file.

Default:
```python
jsonschema = "oarepo_model_builder.builders.jsonschema_builder:JSONSchemaBuilder"
mapping = "oarepo_model_builder.builders.mapping:MappingBuilder"
```

#### oarepo_model_builder.{output_type}

Classes responsible for generating output files of certain type

Default:
```toml
[tool.poetry.plugins."oarepo_model_builder.jsonschema"]
jsonschema = "oarepo_model_builder.outputs:JsonSchemaOutput"

[tool.poetry.plugins."oarepo_model_builder.mapping"]
mapping = "oarepo_model_builder.outputs:MappingOutput"
```


#### oarepo_model_builder.datamodels
Python modules containing data model specification files

## Usage

To build a data model files from a specification file, this package provides the `models` script:

```shell
$ models build --help
Usage: models build [OPTIONS] SOURCE

  Build data model files from JSON5 source specification.

Options:
  --package TEXT            Package name of the model (example: 'test-package')
  --config PATH             Path to custom build config file (example: './build-config.json')
  --datamodel-version TEXT  Version string of the built model: (example: '1.0.0')
  --help
```

