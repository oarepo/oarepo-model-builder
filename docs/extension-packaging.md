# Packaging your extension

This chapter tells you how to package your builder extension. In examples it will use poetry for packaging. If you use
setuptools or any other tool, just follow the same principles.

<!--TOC-->

- [Packaging your extension](#packaging-your-extension)
  - [model-only extension](#model-only-extension)
  - [builder-only extension (no runtime dependencies)](#builder-only-extension-no-runtime-dependencies)
  - [extension with runtime dependencies](#extension-with-runtime-dependencies)
    - [Separating the extension to two packages](#separating-the-extension-to-two-packages)
    - [Keeping runtime and builder parts in a single package](#keeping-runtime-and-builder-parts-in-a-single-package)

<!--TOC-->

## model-only extension

This extension provides a model file(s) to be included by other extensions. The extension should heve the following
layout:

```
my-extension
  +-- my_extension
        +-- __init__.py (empty)
        +-- my-extension-model-1.0.0.yaml/json
  +-- pyproject.toml
  +-- README.md
```

The content of the `my-extension-model.yaml` differs by usage:

* if the model should be included top-level, it should contain the `model` element
* if the model should be included somewhere else (but without the #jsonpath), it should contain directly the content to
  be included

The content of the README.md file should contain a pypi-compatible markdown describing the model. Other files (license,
contribution rules etc.) should be present as well

The content of pyproject.toml goes as:

```toml
[tool.poetry]
name = "my_extension"
version = "0.1.0"
description = ""
authors = ["Mirek Simek <miroslav.simek@vscht.cz>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]
oarepo_model_builder = ">= 0.9.1"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.plugins."oarepo.models"]
my-extension-model = "my_extension:my-extension-model-1.0.0.yaml"
```

Then build the extension with

```bash
poetry build
```

and upload the content of `dist` to your repository (or pypi).

## builder-only extension (no runtime dependencies)

This extension consists of a model file (optionally) and a set of plugins -  
output, builder, model or property plugins. The packaging is similar to the previous case.

```
my-extension
  +-- my_extension
        +-- __init__.py                 (empty)
        +-- builder                     [optional]
            +-- __init__.py
            +-- my_builder_plugin.py
        +-- property                    [optional]
            +-- __init__.py
            +-- my_property_plugin.py
        +-- output                      [optional]
            +-- __init__.py
            +-- my_output_plugin.py
        +-- model                       [optional]
            +-- __init__.py
            +-- my_model_plugin.py
  +-- pyproject.toml
  +-- README.md
```

pyproject.toml looks like:

```toml
[tool.poetry]
name = "my_extension"
version = "0.1.0"
description = ""
authors = ["Mirek Simek <miroslav.simek@vscht.cz>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]
oarepo_model_builder = ">= 0.9.1"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# just examples
[tool.poetry.plugins."oarepo_model_builder.builders"]
my-builder = "my_extension.builder.my_builder_plugin:MyBuilder"

[tool.poetry.plugins."oarepo_model_builder.outputs"]
my-output = "my_extension.output.my_output_plugin:MyOutput"

[tool.poetry.plugins."oarepo_model_builder.property_preprocessors"]
my-property = "my_extension.property.my_property_plugin:MyPropertyPreprocessor"

[tool.poetry.plugins."oarepo_model_builder.model_preprocessors"]
my-model = "my_extension.model.my_model_plugin:MyModelPreprocessor"
```

## extension with runtime dependencies

If an extension has a build-time and runtime parts, you might:

* separate them into two packages (easier for users)
* keep them in a single package (easier for maintainers but might be confusing for user)

### Separating the extension to two packages

Either with two code bases or in your build process, split the extension into two packages. For our sample extension
that handles multilingual properties we would for example have:

* `oarepo-multilingual` - this is the runtime package containing, for example, marshmallow field definition, ES dumper
  component etc.
* `oarepo-model-builder-multilingual` - this is the builder component that performs model transformation to python files

To make sure that the multilingual package is included into the generated sources, include a model preprocessor into
the `oarepo-model-builder-multilingual` which adds a runtime dependency:

```python
from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class MultilingualModelPreprocessor(ModelPreprocessor):
    def transform(self, schema, settings):
        schema.schema.setdefault('runtime-dependencies', {})['oarepo-multilingual'] = "^1.0.0"

```

and register it in `oarepo_model_builder.model_preprocessors` entrypoint. This will automatically add
the `runtime-dependencies` option that is picked up by one of the generators and adds dependencies to
generated `pyproject.toml`.

You can add dev dependencies as well by using 'dev-dependencies' key.

### Keeping runtime and builder parts in a single package

To keep the builder and runtime part in the same package you would like to split the dependencies such that only runtime
dependencies are installed in the "runtime" usage and no dependencies are installed in the "builder" case.

To do so, mark your runtime dependencies as optional with the "extra" group named "runtime" and 
add an optional builder extra:

```toml
[tool.poetry]
name = "my_extension"
version = "0.1.0"
description = ""
authors = ["Mirek Simek <miroslav.simek@vscht.cz>"]

[tool.poetry.dependencies]
python = "^3.9"
invenio = { version = "^3.5.0", optional = true }         # this was added as optional
oarepo-model-builder = { version = ">=0.9.1", optional = true }  # this was added as optional

[tool.poetry.extras]
runtime = ["invenio"]                               # here it is put to runtime group
builder = ["oarepo-model-builder"]

[tool.poetry.dev-dependencies]
oarepo_model_builder = ">= 0.9.1"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# just examples
[tool.poetry.plugins."oarepo_model_builder.builders"]
my-extension-builder = "my_extension.builder.my_builder_plugin:MyBuilder"

[tool.poetry.plugins."oarepo_model_builder.outputs"]
my-extension-output = "my_extension.output.my_output_plugin:MyOutput"

[tool.poetry.plugins."oarepo_model_builder.property_preprocessors"]
my-extension-property = "my_extension.property.my_property_plugin:MyPropertyPreprocessor"

[tool.poetry.plugins."oarepo_model_builder.model_preprocessors"]
my-extension-register-dependencies = "my_extension.registration:RegisterDependenciesPreprocessor"
```

and in the `RegisterDependenciesPreprocessor` register it with extras.

```python
from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class RegisterDependenciesPreprocessor(ModelPreprocessor):
    def transform(self, schema, settings):
        schema.schema.setdefault('runtime-dependencies', {})['my-extension'] = {
            'version': "^1.0.0",
            'extras': ['runtime']
        }
```

This way, when you develop the extension for the builder, you will have "builder" extra installed.
When you develop the "runtime" part, you will have the "runtime" extra installed.

User who installs the extension to oarepo-model-builder environment (either with `pip install my-extension` or 
`pip install my-extension[builder]`) will have the builder part installed.

User who uses oarepo-model-builder to generate the model will be covered as well, as the generated
pyproject.toml will include the extension with runtime extras.

But if this extension is used by someone out of the oarepo-model-builder ecosystem, he should be
always guided to install it as ``pip install my-extension[runtime]`` as otherwise no dependencies
will be installed.
