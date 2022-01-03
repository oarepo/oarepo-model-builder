```yaml
python:
    record-prefix: camel_case(last component of package)
    templates: { }   # overridden templates
    marshmallow:
      top-level-metadata: true
      mapping: { }

    record-prefix-snake: snake_case(record_prefix)

    record-class: { settings.package }.record.{record_prefix}Record
      # full record class name with package
    record-schema-class: { settings.package }.schema.{record_prefix}Schema
      # full record schema class name (apart from invenio stuff, contains only metadata field)
    record-schema-metadata-class: { settings.package }.schema.{record_prefix}MetadataSchema
      # full record schema metadata class name (contains model schema as marshmallow)
    record-schema-metadata-alembic: { settings.package_base }
    # name of key in pyproject.toml invenio_db.alembic entry point 
    record-metadata-class: { settings.package }.metadata.{record_prefix}Metadata
      # db class to store record's metadata 
    record-metadata-table-name: { record_prefix.lower() }_metadata
      # name of database table for storing metadata 
    record-permissions-class: { settings.package }.permissions.{record_prefix}PermissionPolicy
      # class containing permissions for the record
    record-dumper-class: { settings.package }.dumper.{record_prefix}Dumper
      # record dumper class for elasticsearch
    record-search-options-class: { settings.package }.search_options.{record_prefix}SearchOptions
      # search options for the record
    record-service-config-class: { settings.package }.service_config.{record_prefix}ServiceConfig
      # configuration of record's service
    record-resource-config-class: { settings.package }.resource.{record_prefix}ResourceConfig
      # configuration of record's resource
    record-resource-class: { settings.package }.resource.{record_prefix}Resource
      # record resource
    record-resource-blueprint-name: { record_prefix }
    # blueprint name of the resource 
    register-blueprint-function: { settings.package }.blueprint.register_blueprint'
      # name of the blueprint registration function
```