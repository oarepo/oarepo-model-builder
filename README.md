# OARepo model builder

A library and command-line tool to generate invenio model project from a single model file.

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
version: 1.0.0
model:
  properties:
    title: { type: 'fulltext' }
settings:
  <generic settings here>
  python: ...
  elasticsearch: ...
plugins: ...
```

There might be more sections (documentation etc.), but only the ``settings``, ``model`` and ``plugins``
are currently processed.

## "settings" section

The settings section contains various configuration settings. Below are the generic settings with their default values.

```yaml
settings:
  package: basename(output dir) with '-' converted to '_'
  kebap-package: to_kebap(package)
  package-path: path to package as python Path instance
  schema-name: { kebap-package }-{schema-version}.json
  schema-file: full path to generated json schema
  mapping-file: full path to generated mapping
  collection-url: camel_case(last component of package)

```

Advanced use cases might require to modify [the python settings](docs/settings-python.md) or
[elasticsearch settings](docs/settings-elasticsearch.md) (for example, to define custom analyzers).

## "model" section

The model section is a json schema that might be annotated with extra information. For example:

```yaml
model: # this is like the root of the json schema 
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
mapping and marshmallow files with a custom ``PropertyPreprocessor`` - see later.

``oarepo:ui`` gives information for the ui output builder.

``oarepo:documentation`` is a section that is currently ignored. In general, sections that are not recognized are
ignored by default.

### Shortcuts

A ``type: object`` is redundant in models. If there is a `properties` child, the object type is added automatically.

If an `items` child is present, the parent type is set to `array` (if not already present).

If a key inside `properties` looks like `anything[]`, an array will be generated. For example,

```yaml
properties:
  authors[]:
    type: author
    oarepo:documentation: anything here
```

will be translated into:

```yaml
properties:
  authors:
    type: array
      items:
        type: author
        oarepo:documentation: anything here
```

Note that all children are propagated into the `items` section. 
If you want to keep it at the same level, add an array suffix as well:

```yaml
properties:
  authors[]:
    type: author
    oarepo:documentation[]: anything here
```

will be translated into:

```yaml
properties:
  authors:
    type: array
      items:
        type: author
    oarepo:documentation: anything here
```

### Referencing another model

Another model might be included via the `oarepo:use` directive. 

To include another model in your model file, you can:
  * use relative path to reference the model. The whole file will be parsed as json/yaml and
    included at this position
```yaml
model:
  properties:
    author:
      oarepo:use: ./person.yaml

-- with ./person.yaml
type: object
properties:
  firstname: 
    type: string

-- will result into
model:
  properties:
    author:
      oarepo:included-from: ./person.yaml
      type: object
      properties:
        firstname: 
          type: string
```
  * use a model supplied from a pip-installed package. The package references the model
    from entry points. The key in entry points is then used as a reference:
```toml
# poetry

[tool.poetry]
name = "my-included-model"
version = "0.0.1"

include=["my_included_model/model.yaml"]

[tool.poetry.plugins."oarepo.models"]
test = "my_included_model.model.yaml"
```

```yaml
# model

model:
  properties:
    author:
      oarepo:use: test
```

To include a part of another model in the file, you might
  * use a json path to identify the part within the included model. The json path is after
    the `#` character, for example:
```yaml
model:
  properties:
    author:
      oarepo:use: ./common.yaml#/definitions/person
```
  * a reference to the same file is possible as well:
```yaml
model:
  properties:
    author:
      oarepo:use: #/definitions/person
```
  * use an `$id` element in the included model to provide an id and reference the id
```yaml
# included file

definitions:
  person: 
    $id: person

#  model
model:
  properties:
    author:
      oarepo:use: ./common.yaml#person
```

#### Using named types

## Plugins section

See [plugins and the processing order](docs/settings-plugins.md) for details.

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
