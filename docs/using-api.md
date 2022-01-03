# Using API

<!--TOC-->

- [Using API](#using-api)
  - [Load the model](#load-the-model)
    - [Pre-configured from entrypoints](#pre-configured-from-entrypoints)
    - [Options provided manually](#options-provided-manually)
  - [Filesystem access](#filesystem-access)
  - [Create a builder](#create-a-builder)
    - [Pre-configured from entrypoints](#pre-configured-from-entrypoints-1)
    - [Options provided manually](#options-provided-manually-1)
  - [Run the builder](#run-the-builder)

<!--TOC-->

To generate invenio model from a model file, perform the following steps:
  * load the model
  * create an instance of filesystem access [optional]
  * create an instance of builder
  * run the builder

## Load the model

### Pre-configured from entrypoints

```python
from oarepo_model_builder.entrypoints import load_model

model = load_model('mymodel.yaml')
```

Additional options can be supplied:
  * _package_ - name of the package to be generated. Overwrites the package name in model file
  * _configs_ - a list of config files that will be loaded and merged into the model
  * _black_ - run black formatter on generated sources. Only supported if writing generated
    files to normal filesystem
  * _isort_ - run isort for sorting imports on generated sources. Only supported if writing generated
    files to normal filesystem 
  * _model_content_ - optionally provide content of the model. The file name will still be used for
    resolving relative references but will not be loaded

### Options provided manually 

```python
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.loaders import yaml_loader

included_models = {
    'my_model': lambda parent_model: {'test': 'abc'} 
}
loaders = {'yaml': yaml_loader}

model = ModelSchema(file_path='test.yaml', 
                    included_models=included_models, 
                    loaders=loaders)
```

   You can also path directly the content of the file path in ``content`` attribute

   The ``included_models`` is a mapping between model key and its accessor. It is used to replace any ``oarepo:use``
   element. See the Referencing a model above.

   The ``loaders`` handle loading of files - the key is lowercased file extension, value a function taking (schema,
   path) and returning loaded content

## Filesystem access

This step is optional. You can inherit from ``oarepo_model_builder.fs.AbstractFileSystem``
and provide your own filesystem access.

## Create a builder

### Pre-configured from entrypoints

```python
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints

builder = create_builder_from_entrypoints(
    # optionally add filesystem=<Your own filesystem>()
)
```

### Options provided manually

```python
  from oarepo_model_builder.builder import ModelBuilder
  from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
  from oarepo_model_builder.builders.mapping import MappingBuilder
  from oarepo_model_builder.outputs.jsonschema import JSONSchemaOutput
  from oarepo_model_builder.outputs.mapping import MappingOutput
  from oarepo_model_builder.outputs.python import PythonOutput
  from oarepo_model_builder.property_preprocessors.text_keyword import TextKeywordPreprocessor
  from oarepo_model_builder.model_preprocessors.default_values import DefaultValuesModelPreprocessor
  from oarepo_model_builder.model_preprocessors.elasticsearch import ElasticsearchModelPreprocessor
  from oarepo_model_builder.fs import FileSystem

  builder = ModelBuilder(
    output_builders=[JSONSchemaBuilder, MappingBuilder],
    outputs=[JSONSchemaOutput, MappingOutput, PythonOutput],
    model_preprocessors=[DefaultValuesModelPreprocessor, ElasticsearchModelPreprocessor],
    property_preprocessors=[TextKeywordPreprocessor],
    filesystem=FileSystem()
  )    
```   

## Run the builder

```python
  builder.build(model, output_directory)
```
