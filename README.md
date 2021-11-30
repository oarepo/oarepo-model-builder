# OARepo model builder

A library and command-line tool to generate invenio model from a single model file.

## CLI Usage

```bash
oarepo-compile-model model.yaml
```

will compile the model.yaml into the current directory. Options:

```bash
  --output-directory <dir> Output directory where the generated files will be
                           placed. Defaults to "."
  --package <name>         Package into which the model is generated. If not
                           passed, the name of the current directory,
                           converted into python package name, is used.
  --set <name=value>       Overwrite option in the model file. 
                           Example --set settings.elasticsearch.keyword-ignore-above=20
  -v                       Increase the verbosity. This option can be used
                           multiple times.
  --config <filename>      Load a config file and replace parts of the model
                           with it. The config file can be a json, yaml or a
                           python file. If it is a python file, it is
                           evaluated with the current model stored in the
                           "oarepo_model" global variable and after the
                           evaluation all globals are set on the model.
  --isort / --skip-isort   Call isort on generated sources (default: yes)
  --black / --skip-black   Call black on generated sources (default: yes)
```

## Model file structure

A model is a json/yaml file with the following structure:

```yaml
settings:
  python:
  elasticsearch:
model:
  properties:
    title: { type: 'fulltext' }
```

There might be more sections (documentation etc.), but only the ``settings`` and ``model`` are currently processed.

### settings section

The settings section might contain the following keys
(default values below):

```yaml
settings:
  package: basename(output dir) with '-' converted to '_'
  kebap-package: to_kebap(package)
  package-path: path to package as python Path instance
  schema-version: 1.0.0
  schema-name: { kebap-package }-{schema-version}.json
  schema-file: full path to generated json schema
  mapping-file: full path to generated mapping
  collection-url: camel_case(last component of package)

  processing-order: [ 'settings', '*', 'model' ]

  python:
    record-prefix: camel_case(last component of package)
    templates: { }   # overridden templates
    marshmallow:
      top-level-metadata: true
      mapping: { }

    record-prefix-snake: snake_case(record_prefix)

    record-class: { settings.package }.record.{record_prefix}Record
      # full record class name with package
    record-schema-class: { settings.package }.schema.{record_prefix}Schema
      # full record schema class name (apart from invenio stuff, contains only metadata field)
    record-schema-metadata-class: { settings.package }.schema.{record_prefix}MetadataSchema
      # full record schema metadata class name (contains model schema as marshmallow)
    record-schema-metadata-alembic: { settings.package_base }
    # name of key in pyproject.toml invenio_db.alembic entry point 
    record-metadata-class: { settings.package }.metadata.{record_prefix}Metadata
      # db class to store record's metadata 
    record-metadata-table-name: { record_prefix.lower() }_metadata
      # name of database table for storing metadata 
    record-permissions-class: { settings.package }.permissions.{record_prefix}PermissionPolicy
      # class containing permissions for the record
    record-dumper-class: { settings.package }.dumper.{record_prefix}Dumper
      # record dumper class for elasticsearch
    record-search-options-class: { settings.package }.search_options.{record_prefix}SearchOptions
      # search options for the record
    record-service-config-class: { settings.package }.service_config.{record_prefix}ServiceConfig
      # configuration of record's service
    record-resource-config-class: { settings.package }.resource.{record_prefix}ResourceConfig
      # configuration of record's resource
    record-resource-class: { settings.package }.resource.{record_prefix}Resource
      # record resource
    record-resource-blueprint-name: { record_prefix }
    # blueprint name of the resource 
    register-blueprint-function: { settings.package }.blueprint.register_blueprint'
      # name of the blueprint registration function

  elasticsearch:
    keyword-ignore-above: 50

  plugins:
    packages: [ ]
    # list of extra packages that should be installed in compiler's venv
    output|builder|model|property:
      # plugin types - file outputs, builders, model preprocessors, property preprocessors 
      disabled: [ ]
      # list of plugin names to disable
      # string "__all__" to disable all plugins in this category    
      enabled:
      # list of plugin names to enable. The plugins will be used
      # in the order defined. Use with disabled: __all__
      # list of "module:className" that will be added at the end of
      # plugin list
```

### model section

The model section is a json schema that might be annotated with extra sections. For example:

```yaml
model:
  properties:
    title:
      type: multilingual
      oarepo:ui:
        label: Title
        class: bold-text
      oarepo:documentation: |
        Lorem ipsum ...
        Dolor sit ...
```

**Note**: ``multilingual`` is a special type (not defined in this library) that is translated to the correct schema,
mapping and marshmallow files with a custom ``PropertyPreprocessor``.

``oarepo:ui`` gives information for the ui output

``oarepo:documentation`` is a section that is currently ignored

## Referencing a model

## API Usage

To generate invenio model from a model file, perform the following steps:

1. Load the model into a ``ModelSchema`` instance
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


2. Create an instance of ``ModelBuilder``

   To use the pre-installed set of builders and preprocessors, invoke:

   ```python
   from oarepo_model_builder.entrypoints \ 
    import create_builder_from_entrypoints
   
   builder = create_builder_from_entrypoints()
   ```

   To have a complete control of builders and preprocessors, invoke:

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

      builder = ModelBuilder(
        output_builders=[JSONSchemaBuilder, MappingBuilder],
        outputs=[JSONSchemaOutput, MappingOutput, PythonOutput],
        model_preprocessors=[DefaultValuesModelPreprocessor, ElasticsearchModelPreprocessor],
        property_preprocessors=[TextKeywordPreprocessor]
      )    
   ```   


3. Invoke

   ```python
      builder.build(schema, output_directory)
   ```

## Extending the builder

### Builder pipeline

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
the top-level properties of the transformed schema are then iterated. 
The order of the top-level properties is given by ``settings.processing-order``.

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

### Registering Preprocessors, Builders and Outputs for commandline client

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

### Generating python files

The default python output is based on [libCST](https://github.com/Instagram/LibCST) that enables merging generated code
with a code that is already present in output files. The transformer provided in this package can:

1. Add imports
2. Add a new class or function on top-level
3. Add a new method to an existing class
4. Add a new const/property to an existing class

The transformer will not touch an existing function/method. Increase verbosity level to get a list of rejected patches
or add ``--set settings.python.overwrite=true``
(use with caution, with sources stored in git and do diff afterwards).

#### Overriding default templates

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
