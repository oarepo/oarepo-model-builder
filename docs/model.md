# Model

<!--TOC-->

- [Model](#model)
  - [Validation](#validation)
  - [Required fields](#required-fields)
  - [Shortcuts](#shortcuts)
  - [Referencing another model](#referencing-another-model)
  - [Built-in extensions](#built-in-extensions)
    - [`oarepo:mapping` - elasticsearch definition](#oarepomapping---elasticsearch-definition)
    - [`oarepo:marshmallow` - marshmallow definition](#oarepomarshmallow---marshmallow-definition)
  - [Sample data](#sample-data)

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

## Validation

The model file is validated before it is processed. It is possible
to override the validation by providing `oarepo:model-validation`
section with extended validation rules. See oarepo_model_builder/validation/schemas
for hints on the rules.

## Required fields

For the sake of lucidity, model does not place required
elements to one "required" array but expects the requirement
defined on the concrete element (such as in marshmallow schema).
For example:

```yaml
model: # this is like the root of the json schema 
  properties:
    title:
      type: text
      required: true
```


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

Note that all children are propagated into the `items` section. If you want to keep it at the same level, add an array
suffix as well:

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

* use relative path to reference the model. The whole file will be parsed as json/yaml and included at this position

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

* use a model supplied from a pip-installed package. The package references the model from entry points. The key in
  entry points is then used as a reference:

```toml
# poetry

[tool.poetry]
name = "my-included-model"
version = "0.0.1"

include = ["my_included_model/model.yaml"]

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

* use a json path to identify the part within the included model. The json path is after the `#` character, for example:

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

**Note:** If you reference multiple files via ``oarepo:use: ["a", "b"]`` and both
include the same property, the value from ``a`` will be used.

## Built-in extensions

### `oarepo:mapping` - elasticsearch definition

Everything that is present in the `oarepo:mapping` section is written to the ES mapping file. For example:

```json
{
  "model": {
    "properties": {
      "title": {
        "type": "string",
        "oarepo:mapping": {
          "type": "text",
          "analyzer": "chinese"
        }
      }
    }
  }
}
```

will generate the following mapping (note that schema type is overwritten with the mapping type):

```json
{
  "mapping": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "chinese"
      }
    }
  }
}
```

### `oarepo:marshmallow` - marshmallow definition

This customizes how the marshmallow field will be generated. The section might contain:

* `field` - a string containing the field instance, for example `"blah = MyField(param='value')"`. This is used as is,
  no modifications are performed to the field
* `class` - a field will be instantiated with this class. If a class is `BlahField`, the created field might look
  like `blah = BlahField(..., required=True)`
* `nested` - the class above is not a field but schema and it will be wrapped with `ma_fields.Nested()`
* `imports` - a dictionary of "import" : "alias" will generate `import <import> as <alias>`
* `imported-classes` - a dictionary of "import.classname": "alias" will
  generate `from <import> import <classname> as <alias?`
* `generate` - if the current element is a jsontype object ("type": "object"), tell the builder to generate this class
  as well (if not set it is expected that the class already exists in sources)

Example:

```yaml
model:
  properties:
    person:
      type: object
      properties:
      # ...
      oarepo:marshmallow:
        generate: true
        class: people.PersonSchema
```

will generate the people.PersonSchema class from the properties.

```yaml
model:
  properties:
    person:
      type: object
      properties:
      # ...
      oarepo:marshmallow:
        nested: true
        class: people.PersonSchema
```

will suppose that the PersonSchema already exists and will create ``person = ma_fields.Nested(PersonSchema())``
It will automatically import "people" package at the top of the file

```yaml
model:
  properties:
    person:
      type: object
      properties:
      # ...
      oarepo:marshmallow:
        nested: true
        field: people.PersonField()
        imports:
          people: people
```

A field will just be used and is opaque to the builder. That is why 'imports' section must be specified as well.

#### Pre-defined import aliases

The following aliases are pre-defined and need not be declared:

* import marshmallow as ma
* import marshmallow.fields as ma_fields
* import marshmallow.validate as ma_valid

If the prefix is used as a part of `class`, it is automatically recognized.

## Sample data

For testing purposes, oarepo-model-builder also generate a yaml file with 
sample data. The data are generated by a "faker" python package and 
the process can be customized by inserting a "oarepo:sample" section
into the model file.

The following will always insert "John Smith" into the sample data:

```yaml
model:
  properties:
    author:
      type: keyword
      oarepo:sample: John Smith
```

If you want to select from multiple values, add them as an array:

```yaml
model:
  properties:
    author:
      type: keyword
      oarepo:sample: [John Smith, Anne White]
```

You can call a Faker object directly via:

```yaml
model:
  properties:
    author:
      type: keyword
      oarepo:sample: 
        faker: name
```

This will call Faker's person provider and fill in the name.
See [https://faker.readthedocs.io/en/master/providers/baseprovider.html](https://faker.readthedocs.io/en/master/providers/baseprovider.html)
for details.

If the faker method is parametrized, add the keyword parameters via:

```yaml
model:
  properties:
    author:
      type: keyword
      oarepo:sample: 
        faker: bothify
        params:
          letters: ABCDE
```
