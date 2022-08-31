# Property plugins

Property plugins work for each property in the `model` part of the model file and can modify,
remove or split it into several properties before it is processed by an output builder.

The plugin might generate a different output for each of the builders.

<!--TOC-->

- [Property plugins](#property-plugins)
  - [Writing plugin](#writing-plugin)
    - [Removing the element entirely](#removing-the-element-entirely)
    - [Splitting the element into multiple elements](#splitting-the-element-into-multiple-elements)
  - [Plugin registration](#plugin-registration)

<!--TOC-->

## Writing plugin

```python
from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge

class DatePreprocessor(PropertyPreprocessor):
    TYPE = 'date'

    @process(model_builder=JSONSchemaBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'date')
    def modify_date_jsonschema(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'string'
        data.setdefault('format', 'date')
        return data

    @process(model_builder=InvenioRecordSchemaBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'date')
    def modify_date_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        deepmerge(
            data.setdefault('oarepo:marshmallow', {}),
            {
                'class': 'ma_fields.Date'
            }
        )
        return data
```

Each plugin has its own `TYPE` so that it can be enabled/disabled in the plugin configuration.
It may contain one or mode methods decorated with a `process` decorator. The decorator takes
the following arguments:

  * `model_builder`: either a `TYPE` or a class of the model builder, for which the model is transformed.
    You can also pass `*` to invoke the method for all builders. 
  * `path`: the method is called only for paths matching this glob. '*' is a single element, '**' any number
    of elements in the path. In this example, paths `/model/properties/a` and `/model/properties/a/properties/b`
    will match, `/model/properties/a/type` will not
  * `condition` is the condition to be evaluated when path matches. The condition receives
     * `current`, that represents the currently processed model element (instance of Munch/array/primitive)
     * `stack` and instance of `oarepo_model_builder.stack.ModelBuilderStack` if you want a condition
       that needs a context

The method receives a `data` argument that might be freely modified. In the example above, 
the `modify_date_jsonschema` method is invoked when `type=date` and changes the type to jsonschema
string (as json represents dates serialized as strings). It also adds a `format` parameters if it is 
not yet present.

The marshmallow preprocessor leaves the type but merges in (via deepmerge function) ``oarepo:marshmallow.class``
with the correct marshmallow Date field.


### Removing the element entirely

A plugin can return `ModelBuilderStack.SKIP` to force skipping of the element

### Splitting the element into multiple elements

In some cases it might be useful to generate more elements out of a single model element. This
might be useful mostly in mappings, where for example the following data:

```json
{
  "title": [{"lang":  "cs", "value":  "Nazev"}, {"lang":  "en", "value":  "Title"}, ...]
}
```

might be represented in ES mapping as:

```json
{
  "title": { "type":  "object", ...},
  "title_cs": {"type":  "text", "analyzer":  "icu_czech"}
}
```

That is, title can be in any languages but only "cs" will be treated prominently with custom analyzer
(and this will be handled in a Dumper to extract the czech title and serialize into title_cs property).

To replace element, raise a `ReplaceElement` exception containing the replacement. 

Note: the replacement will be again processed by the property preprocessors, so make sure that you
do not raise the exception over and over. In the example below, the `type` in the condition is changed
from `multilingual` to `object`, and the preprocessor is called only once

```python
    @process(model_builder=MappingBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'multilingual')
    def modify_multilang_mapping(self, data, stack, **kwargs):
        raise ReplaceElement({
            stack.top.key: {
                'type': 'object',
                'properties': {
                    'lang': {
                        'type': 'keyword'
                    },
                    'value': {
                        'type': 'text'
                    }
                }
            },
            stack.top.key + '_cs': {
                'type': 'text'
            }
        })
```

## Plugin registration 

A plugin is registered in entrypoints in group `oarepo_model_builder.property_preprocessors`. 
In setup.cfg, this is written as:

```cfg
[entry_points]
oarepo_model_builder.property_preprocessors = 
    600-date = oarepo_model_builder.property_preprocessors.date:DatePreprocessor
```

Note: plugins are loaded in the order given by the key and are evaluated in the same order.

