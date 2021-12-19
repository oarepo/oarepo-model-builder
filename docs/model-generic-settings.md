# Default generic settings


Below are the generic settings with their default values.

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

Advanced use cases might require to modify [the python settings](model-python-settings.md) or
[elasticsearch settings](model-elasticsearch-settings.md) (for example, to define custom analyzers).
