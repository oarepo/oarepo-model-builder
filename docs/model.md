# Model

<!--TOC-->

- [Model](#model)
  - [Shortcuts](#shortcuts)
  - [Referencing another model](#referencing-another-model)
  - [Built-in extensions](#built-in-extensions)
    - [`oarepo:mapping` - elasticsearch definition](#oarepomapping---elasticsearch-definition)
    - [`oarepo:marshmallow` - marshmallow definition](#oarepomarshmallow---marshmallow-definition)

<!--TOC-->


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

## Shortcuts

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

## Referencing another model

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

-- will create the following model
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
test = "my_included_model:model.yaml"
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
  * a reference within the same file is possible as well:
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
    properties:
      first_name: { type: string }

#  model
model:
  properties:
    author:
      oarepo:use: ./common.yaml#person
```

## Built-in extensions

### `oarepo:mapping` - elasticsearch definition

### `oarepo:marshmallow` - marshmallow definition