# Plugins

This section of model file configures which plugins are used during the processing and in which
order is the model file processed. Apart from `packages`, there is usually no need to modify this. 

```yaml
processing-order: [ 'settings', '*', 'model' ]


plugins:
    packages: [ ]
    # list of extra packages that should be installed in compiler's venv
    output|builder|model|property:
      # plugin types - file outputs, builders, model preprocessors, property preprocessors 
      disable: [ ]
      # list of plugin names to disable
      # string "__all__" to disable all plugins in this category    
      enable:
      # list of plugin names to enable. The plugins will be used
      # in the order defined.
      include:
      # list of "module:className" that will be added. If you want to define he order,
      # use disable: __all__ and add the plugin name to enable section      
```

## `processing_order`

This setting defines in which order the builders process sections of the model file. A star `*` can be used
to indicate that all additional parts are processed at this point. In the example above, at first settings
are processed, then anything else but model and finally the model section of the file.

Unless you define your own sections that are dependent on other sections, you can leave this setting as it is.

## `plugins`

This section defines which plugins will be used to process the model file. Normally you do not have 
to modify this setting as plugins are discovered automatically. 

Plugins are divided into four different classes: output, builder, model and property.
If you look into the source code:
  * *output* plugins inherit from `OutputBase` and are usually called `<Something>Output`
  * *builder* plugin class name usually ends with `Builder` and they inherit from `OutputBuilder`
  * *model* preprocessor plugins inherit from `ModelPreprocessor` and their class name ends with `ModelPreprocessor`
  * *property* preprocessor plugins inherit from `PropertyPreprocessor` and their class name ends with `Preprocessor`
  
Plugins are enabled/disabled by their `type` - to get it, see the source code of the plugin 
and look for `TYPE` constant:

```python
from .invenio_base import InvenioBaseClassPythonBuilder

class InvenioRecordPermissionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = 'invenio_record_permissions'
    class_config = 'record-permissions-class'
    template = 'record-permissions'
```

### Disabling a plugin

Put the plugin type into the `disable` section:

```yaml
plugins:
  builder:    # name of the class
    disable: [ invenio_record_permissions ]
```

Now, the permissions will be disabled and permission class will not be generated.

### Enabling only several plugins

At first disable all the plugins and then enable only the specific ones:

```yaml
plugins:
  builder:    # name of the class
    disable: __all__
    enable: [ invenio_record_permissions ]
```

### Adding a custom plugin

To add a custom plugin that is not in a distribution package (therefore not registered automatically),
add its full python name to the `include` section. For example, if you have a custom Vocabulary plugin,
include it with:

```yaml
plugins:
  property:
    include:
      - temp.vocabulary:VocabularyPropertyPreprocessor
```
