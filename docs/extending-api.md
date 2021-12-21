# Extending the API

## Quick start
 *  [template for property plugins](./extending-property.md)
 *  [template for builder plugins](./extending-builder.md)

-----

<!--TOC-->

- [Extending the API](#extending-the-api)
  - [Quick start](#quick-start)
  - [Builder pipeline](#builder-pipeline)
  - [Creating your own property preprocessor](#creating-your-own-property-preprocessor)
  - [Create your own Builders](#create-your-own-builders)

<!--TOC-->


## Builder pipeline

![Pipeline](./oarepo-model-builder.png)

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

## Creating your own property preprocessor

See [template for property plugins](./extending-property.md)

## Create your own Builders

See [template for builder plugins](./extending-builder.md)
