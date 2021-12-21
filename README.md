# OARepo model builder

A library and command-line tool to generate invenio model project from a single model file.

<!--TOC-->

- [OARepo model builder](#oarepo-model-builder)
  - [CLI Usage](#cli-usage)
  - [Model file](#model-file)
    - [Model file structure](#model-file-structure)
    - ["model" section](#model-section)
    - ["settings" section](#settings-section)
    - ["plugins" section](#plugins-section)
  - [Builder as a library (using via API)](#builder-as-a-library-using-via-api)
  - [Extending the builder](#extending-the-builder)

<!--TOC-->

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

## Model file

A model is a json/yaml file including description of the model and processing settings.
Example:

```yaml
version: 1.0.0
model: 
  properties:
    title:
      type: fulltext+keyword
      oarepo:ui:
        label: Title
      oarepo:mapping:
         # anything in here will be put into the mapping file
         # fulltext+keyword type automatically creates "type: text" 
         # with subfield 'keyword' of type keyword
settings:
  package: uct.titled_model 
```


### Model file structure

A model is a json/yaml file with the following structure:

```yaml
version: 1.0.0
model:
  properties:
    title: 
      type: fulltext+keyword
settings:
  <generic settings here>
  python: ...
  elasticsearch: ...
plugins: ...
```

There might be more sections (documentation etc.), but only the ``settings``, ``model`` and ``plugins``
are currently processed.

### "model" section

This section is described in [model.md](docs/model.md)

### "settings" section

The settings section contains various configuration settings. In most cases you want to set only 
the `package` option as in above because all other settings are derived from it. Even the `package`
option might be omitted - in this case the package name will be the last component of the output 
directory (with dashes converted to underscores).

The rest of the settings are described in [model-generic-settings.md](docs/model-generic-settings.md)

Advanced use cases might require to modify [the python settings](docs/model-python-settings.md) or
[elasticsearch settings](docs/model-elasticsearch-settings.md) (for example, to define custom analyzers).

### "plugins" section

See [plugins and the processing order](docs/model-plugins.md) for details.

## Builder as a library (using via API)

To invoke the builder programmatically, see [using the API](docs/using-api.md).

## Extending the builder

See [writing plugins](docs/extending-api.md) if you want to extend the building process with your
own plugins.