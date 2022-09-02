# Builder plugins

A builder is responsible for generating output file. It does not write to the filesystem
directly but through Output classes - this way even if multiple builders modify a single
file, the access is coordinated.

<!--TOC-->

- [Builder plugins](#builder-plugins)
  - [Writing plugin](#writing-plugin)
  - [Plugin registration](#plugin-registration)
  - [Generating python files](#generating-python-files)
  - [Overriding default templates](#overriding-default-templates)

<!--TOC-->

## Writing plugin

```python
class JSONSchemaBuilder(OutputBuilder):
    output_file_name: str = None
    output_file_type: str = None
    parent_module_root_name: str = None

    @process('/model')
    def enter_model(self):
        output_name = self.settings[self.output_file_name]
        self.output = self.builder.get_output('json', output_name)

    @process('/model/**', condition=lambda current, stack: is_schema_element(stack))
    def model_element(self):
        # TODO: write the element at the top of the stack to the output
        self.build_children()
        # TODO: tell the output that the element ended        
```

The file above shows how a schema builder might be implemented. When a model element is entered,
an output is allocated via `self.builder.get_output` call. Then on schema elements (filtered by
processing condition) these are written into the output. See `../oarepo_model_builder/builders/jsonschema.py`
for complete sources.

## Plugin registration

A plugin is registered in entrypoints in group `oarepo_model_builder.builders`. 
In setup.cfg, this is written as:

```cfg
[entry_points]
oarepo_model_builder.builders = 
    020-jsonschema = oarepo_model_builder.builders.jsonschema:JSONSchemaBuilder
```

Note: plugins are loaded in the order given by the key and are evaluated in the same order.


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
