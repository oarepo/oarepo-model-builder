# Default generic settings

Below are the generic settings with their default values.

```yaml
settings:
  package: basename(output dir) with '-' converted to '_'
  schema-version: taken from top-level version
  top-level-metadata: true will generate schema with top-level metadata section

  # derived from package
  collection-url: camel_case(last component of package)

  package-base: cis_repository_theses_model
  package-base-upper: CIS_REPOSITORY_THESES_MODEL
  schema-server: http://localhost/schemas/

  kebap-package: to_kebap(package)
  package-path: path to package as python Path instance

  schema-name: { kebap-package }-{schema-version}.json
  schema-file: full path to generated json schema
  jsonschemas-package: cis_repository_theses_model.model.jsonschemas

  mapping-file: full path to generated mapping
  index-name: { package-base }-{kebap-package}-{schema-version}
  mapping-package: { package }.model.mappings
```

Advanced use cases might require to modify [the python settings](model-python-settings.md) or
[elasticsearch settings](model-elasticsearch-settings.md) (for example, to define custom analyzers).
