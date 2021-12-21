# Extending the API

See [template for property plugins](./extending-property.md)

See [template for builder plugins](./extending-builder.md)

<!--TOC-->

- [Extending the API](#extending-the-api)
  - [Builder pipeline](#builder-pipeline)
  - [Registering Preprocessors, Builders and Outputs for commandline client](#registering-preprocessors-builders-and-outputs-for-commandline-client)
  - [Generating python files](#generating-python-files)
  - [Overriding default templates](#overriding-default-templates)

<!--TOC-->


## Builder pipeline

![Pipeline](./docs/oarepo-model-builder.png)

At first, an instance of [ModelSchema](./oarepo_model_builder/schema.py) is obtained. The schema can be either passed
the content of the schema as text, or just a path pointing to the file. The extension of the file determines
which [loader](./oarepo_model_builder/loaders/__init__.py) is used. JSON, JSON5 and YAML are supported out of the box (
if you have json5 and pyyaml packages installed)

Then [ModelBuilder](./oarepo_model_builder/builder.py).build(schema, output_dir) is called.

It begins with calling all [ModelPreprocessors](./oarepo_model_builder/model_preprocessors/__init__.py). They get the
whole schema and settings and can modify both.
See [ElasticsearchModelPreprocessor](./oarepo_model_builder/model_preprocessors/elasticsearch.py) as an example. The
deepmerge function does not overwrite values if they already exist in settings.

For each of the outputs (jsonschema, mapping, record, resource, ...)
the top-level properties of the transformed schema are then iterated. The order of the top-level properties is given
by ``settings.processing-order``.

The top-level property and all its descendants (a visitor patern, visiting property by property),
a [PropertyPreprocessor](./oarepo_model_builder/property_preprocessors/__init__.py)
is called.

The preprocessor can either modify the property, decide to remove it or replace it with a new set of properties
(see [multilang in tests](./tests/multilang.py) ).

The property is then passed to the
[OutputBuilder](./oarepo_model_builder/builders/__init__.py)
(an example is [JSONSchemaBuilder](./oarepo_model_builder/builders/jsonschema.py))
that serializes the tree of properties into the output.

The output builder does not create files on the filesystem explicitly but uses instances
of [OutputBase](./oarepo_model_builder/outputs/__init__.py), for
example [JSONOutput](./oarepo_model_builder/outputs/json.py) or more
specialized [JSONSchemaOutput](./oarepo_model_builder/outputs/jsonschema.py).

See [JSONBaseBuilder](./oarepo_model_builder/builders/json_base.py) for an example of how to get an output and write to
it (in this case, the json-based output).

This way, even if more output builders access the same file, their access is coordinated.

## Registering Preprocessors, Builders and Outputs for commandline client

The model & property preprocessors, output builders and outputs are registered in entry points. In poetry, it looks as:

```toml
[tool.poetry.plugins."oarepo_model_builder.builders"]
010-jsonschema = "oarepo_model_builder.builders.jsonschema:JSONSchemaBuilder"
020-mapping = "oarepo_model_builder.builders.mapping:MappingBuilder"
030-python_structure = "oarepo_model_builder.builders.python_structure:PythonStructureBuilder"
040-invenio_record = "oarepo_model_builder.invenio.invenio_record:InvenioRecordBuilder"

[tool.poetry.plugins."oarepo_model_builder.ouptuts"]
jsonschema = "oarepo_model_builder.outputs.jsonschema:JSONSchemaOutput"
mapping = "oarepo_model_builder.outputs.mapping:MappingOutput"
python = "oarepo_model_builder.outputs.python:PythonOutput"

[tool.poetry.plugins."oarepo_model_builder.property_preprocessors"]
010-text_keyword = "oarepo_model_builder.preprocessors.text_keyword:TextKeywordPreprocessor"

[tool.poetry.plugins."oarepo_model_builder.model_preprocessors"]
01-default = "oarepo_model_builder.transformers.default_values:DefaultValuesModelPreprocessor"
10-invenio = "oarepo_model_builder.transformers.invenio:InvenioModelPreprocessor"
20-elasticsearch = "oarepo_model_builder.transformers.elasticsearch:ElasticsearchModelPreprocessor"

[tool.poetry.plugins."oarepo_model_builder.loaders"]
json = "oarepo_model_builder.loaders:json_loader"
json5 = "oarepo_model_builder.loaders:json_loader"
yaml = "oarepo_model_builder.loaders:yaml_loader"
yml = "oarepo_model_builder.loaders:yaml_loader"

[tool.poetry.plugins."oarepo_model_builder.templates"]
99-base_templates = "oarepo_model_builder.invenio.templates"
```

## Generating python files

The default python output is based on [libCST](https://github.com/Instagram/LibCST) that enables merging generated code
with a code that is already present in output files. The transformer provided in this package can:

1. Add imports
2. Add a new class or function on top-level
3. Add a new method to an existing class
4. Add a new const/property to an existing class

The transformer will not touch an existing function/method. Increase verbosity level to get a list of rejected patches
or add ``--set settings.python.overwrite=true``
(use with caution, with sources stored in git and do diff afterwards).

## Overriding default templates

The default templates are written as jinja2-based templates.

To override a single or multiple templates, create a package containing the templates and register it
in ``oarepo_model_builder.templates``. Be sure to specify the registration key smaller than ``99-``. The template loader
iterates the sorted set of keys and your templates would be loaded before the default ones. Example:

   ```
   my_package
      +-- __init__.py
      +-- templates
          +-- invenio_record.py.jinja2 
   ```

   ```python
   # my_package/__init__.py
TEMPLATES = {
    # resolved relative to the package
    "record": "templates/invenio_record.py.jinja2"
}
   ```

   ```toml
   [tool.poetry.plugins."oarepo_model_builder.templates"]
20-my_templates = "my_package"
   ```

To override a template for a single model, in your model file (or configuration file with -c option or via --set option)
, specify the relative path to the template:

```yaml
settings:
  python:
    templates:
      record: ./test/my_invenio_record.py.jinja2
```
