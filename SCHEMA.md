## [ModelFileSchema](#ModelFileSchema)

| property | type | documentation |
| --- | --- | --- |
| $defs | [DefsSchema](#DefsSchema) | Extra definitions, might be included via _use_ or _extend_ |
| record | [ModelDataTypeModelValidator](#ModelDataTypeModelValidator) | Main record |
| settings | [SettingsSchema](#SettingsSchema) | General settings, applies to all generated sources |
| version | String | Model version, default value 1.0.0 |
## [ModelDataTypeModelValidator](#ModelDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| api-blueprint | [BlueprintSchema](#BlueprintSchema) | API blueprint details |
| config | [ConfigSchema](#ConfigSchema) | Application config details |
| enum | Array of Raw | A list of possible values |
| ext | [ExtSchema](#ExtSchema) | Application extension details |
| extend | String |  |
| json-schema-settings | [JSONSchema](#JSONSchema) | JSON Schema section of the model. Properties will be generated automatically |
| json-serializer | [JSONSerializerSchema](#JSONSerializerSchema) |  |
| mapping-settings | [ModelMappingSchema](#ModelMappingSchema) | Mapping definition |
| marshmallow | [ModelMarshmallowSchema](#ModelMarshmallowSchema) |  |
| model-name | String | Name of the model, will be used as module name if no module is specified |
| module | [ModuleSchema](#ModuleSchema) | Model module details |
| permissions | [ModelPermissionsSchema](#ModelPermissionsSchema) | Permissions settings |
| pid | [PIDSchema](#PIDSchema) | PID settings |
| properties | [ObjectPropertiesField](#ObjectPropertiesField) |  |
| proxy | [ProxySchema](#ProxySchema) | Settings for service proxy |
| record | [RecordClassSchema](#RecordClassSchema) | api/Record settings |
| record-dumper | [RecordDumperClassSchema](#RecordDumperClassSchema) | Settings for record dumper |
| record-metadata | [RecordMetadataClassSchema](#RecordMetadataClassSchema) | Record metadata settings |
| required | Boolean |  |
| resource | [ResourceClassSchema](#ResourceClassSchema) | Resource class settings |
| resource-config | [ResourceConfigClassSchema](#ResourceConfigClassSchema) | Resource config class settings |
| sample | [SampleSchema](#SampleSchema) | Settings for sample document generator |
| saved-model | [SavedModelSchema](#SavedModelSchema) |  |
| searchable | Boolean | Will the mapping/indexing be generated on model? (can be overriden on individual properties) |
| service | [ServiceClassSchema](#ServiceClassSchema) | Service settings |
| service-config | [ServiceConfigClassSchema](#ServiceConfigClassSchema) | Service config settings |
| type | String |  |
| ui | [ModelUISchema](#ModelUISchema) | UI settings |
| use | String |  |
## [JSONSchema](#JSONSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Alias under which jsonschema is referenced in setup.cfg |
| file | String | Path to schema file |
| generate | Boolean | Generate json schema (default is true) |
| module | String | Schema module |
| name | String | Schema name |
| template | [PermissiveSchema](#PermissiveSchema) | Template that will be merged with the schema |
| version | String | Schema version |
## [PermissiveSchema](#PermissiveSchema)

| property | type | documentation |
| --- | --- | --- |
| extend | String |  |
| use | String |  |
## [ModelMappingSchema](#ModelMappingSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Index alias, under which the mapping is registered in setup.cfg |
| file | String | Path to index file |
| generate | Boolean | Generate mapping (default is true) |
| index | String | Index name |
| module | String | Module with mapping definition |
| template | [PermissiveSchema](#PermissiveSchema) | Mapping template, merged with generated mapping |
## [FieldSchema](#FieldSchema)

| property | type | documentation |
| --- | --- | --- |
| _array_ | [ArrayDataTypeModelValidator](#ArrayDataTypeModelValidator) |  |
| _boolean_ | [BooleanDataTypeModelValidator](#BooleanDataTypeModelValidator) |  |
| _date_ | [DateDataTypeModelValidator](#DateDataTypeModelValidator) |  |
| _datetime_ | [DateTimeDataTypeModelValidator](#DateTimeDataTypeModelValidator) |  |
| _double_ | [DoubleDataTypeModelValidator](#DoubleDataTypeModelValidator) |  |
| _edtf-interval_ | [EDTFIntervalTypeModelValidator](#EDTFIntervalTypeModelValidator) |  |
| _edtf_ | [EDTFDataTypeModelValidator](#EDTFDataTypeModelValidator) |  |
| _flattened_ | [FlattenDataTypeModelValidator](#FlattenDataTypeModelValidator) |  |
| _float_ | [FloatDataTypeModelValidator](#FloatDataTypeModelValidator) |  |
| _fulltext+keyword_ | [FulltextKeywordDataTypeModelValidator](#FulltextKeywordDataTypeModelValidator) |  |
| _fulltext_ | [FulltextDataTypeModelValidator](#FulltextDataTypeModelValidator) |  |
| _integer_ | [IntegerDataTypeModelValidator](#IntegerDataTypeModelValidator) |  |
| _keyword_ | [KeywordDataTypeModelValidator](#KeywordDataTypeModelValidator) |  |
| _model_ | [ModelDataTypeModelValidator](#ModelDataTypeModelValidator) |  |
| _nested_ | [NestedDataTypeModelValidator](#NestedDataTypeModelValidator) |  |
| _object_ | [ObjectDataTypeModelValidator](#ObjectDataTypeModelValidator) |  |
| _time_ | [TimeDataTypeModelValidator](#TimeDataTypeModelValidator) |  |
| _url_ | [URLDataTypeModelValidator](#URLDataTypeModelValidator) |  |
## [IntegerDataTypeModelValidator](#IntegerDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| exclusiveMaximum | Integer |  |
| exclusiveMinimum | Integer |  |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| maximum | Integer |  |
| minimum | Integer |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [PropertyUISchema](#PropertyUISchema)

| property | type | documentation |
| --- | --- | --- |
| extend | String |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) | UI marshmallow |
| use | String |  |
## [PropertyMarshmallowSchema](#PropertyMarshmallowSchema)

| property | type | documentation |
| --- | --- | --- |
| arguments | Array of String |  |
| extend | String |  |
| field | String |  |
| field-class | String |  |
| field-name | String |  |
| imports | Array of [ImportSchema](#ImportSchema) |  |
| read | Boolean |  |
| use | String |  |
| validators | Array of String |  |
| write | Boolean |  |
## [ImportSchema](#ImportSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String |  |
| extend | String |  |
| import | String |  |
| use | String |  |
## [SampleSchema](#SampleSchema)

| property | type | documentation |
| --- | --- | --- |
| extend | String |  |
| faker | String | The faker to use for generating the sample |
| params | Raw | Params for the faker |
| skip | Boolean | Set true to skip generating sample for the field |
| use | String |  |
## [FacetsSchema](#FacetsSchema)

| property | type | documentation |
| --- | --- | --- |
| searchable | Boolean | True if the field is rendered into a facet |
## [FloatDataTypeModelValidator](#FloatDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| exclusiveMaximum | Float |  |
| exclusiveMinimum | Float |  |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| maximum | Float |  |
| minimum | Float |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [DoubleDataTypeModelValidator](#DoubleDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| exclusiveMaximum | Float |  |
| exclusiveMinimum | Float |  |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| maximum | Float |  |
| minimum | Float |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [BooleanDataTypeModelValidator](#BooleanDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [DateDataTypeModelValidator](#DateDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [TimeDataTypeModelValidator](#TimeDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [DateTimeDataTypeModelValidator](#DateTimeDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [EDTFDataTypeModelValidator](#EDTFDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [EDTFIntervalTypeModelValidator](#EDTFIntervalTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [FulltextDataTypeModelValidator](#FulltextDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| maxLength | Integer |  |
| minLength | Integer |  |
| regex | String |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [KeywordDataTypeModelValidator](#KeywordDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| maxLength | Integer |  |
| minLength | Integer |  |
| regex | String |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [FulltextKeywordDataTypeModelValidator](#FulltextKeywordDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| maxLength | Integer |  |
| minLength | Integer |  |
| regex | String |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [ObjectDataTypeModelValidator](#ObjectDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [ObjectMarshmallowSchema](#ObjectMarshmallowSchema) |  |
| properties | [ObjectPropertiesField](#ObjectPropertiesField) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [ObjectUISchema](#ObjectUISchema) |  |
## [ObjectPropertiesField](#ObjectPropertiesField)

| property | type | documentation |
| --- | --- | --- |
| * | [FieldSchema](#FieldSchema) | None |
## [ObjectUISchema](#ObjectUISchema)

| property | type | documentation |
| --- | --- | --- |
| extend | String |  |
| marshmallow | [ObjectMarshmallowSchema](#ObjectMarshmallowSchema) |  |
| use | String |  |
## [ObjectMarshmallowSchema](#ObjectMarshmallowSchema)

| property | type | documentation |
| --- | --- | --- |
| arguments | Array of String |  |
| base-classes | Array of String | List of marshmallow base classes |
| class | String | The name of the marshmallow class |
| extend | String |  |
| extra-fields | Array of [ExtraField](#ExtraField) | Extra fields to generate into the marhsmallow class |
| field | String |  |
| field-class | String |  |
| field-name | String |  |
| generate | Boolean | Generate the marshmallow class (default is true) |
| imports | Array of [ImportSchema](#ImportSchema) |  |
| module | String | Class module |
| read | Boolean |  |
| use | String |  |
| validators | Array of String |  |
| write | Boolean |  |
## [ExtraField](#ExtraField)

| property | type | documentation |
| --- | --- | --- |
| name | String | Name (lhs) of the field |
| value | String | Literal definition (rhs) of the field |
## [NestedDataTypeModelValidator](#NestedDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [ObjectMarshmallowSchema](#ObjectMarshmallowSchema) |  |
| properties | [ObjectPropertiesField](#ObjectPropertiesField) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [ObjectUISchema](#ObjectUISchema) |  |
## [FlattenDataTypeModelValidator](#FlattenDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [ArrayDataTypeModelValidator](#ArrayDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| extend | String |  |
| facets | [FacetsSchema](#FacetsSchema) |  |
| items | [FieldSchema](#FieldSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| maxItems | Integer |  |
| minItems | Integer |  |
| required | Boolean |  |
| sample | [ArraySampleSchema](#ArraySampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
| uniqueItems | Boolean |  |
| use | String |  |
## [ArraySampleSchema](#ArraySampleSchema)

| property | type | documentation |
| --- | --- | --- |
| count | Integer |  |
| extend | String |  |
| use | String |  |
## [URLDataTypeModelValidator](#URLDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| enum | Array of Raw | A list of possible values |
| facets | [FacetsSchema](#FacetsSchema) |  |
| jsonschema | [PermissiveSchema](#PermissiveSchema) |  |
| mapping | [PermissiveSchema](#PermissiveSchema) |  |
| marshmallow | [PropertyMarshmallowSchema](#PropertyMarshmallowSchema) |  |
| maxLength | Integer |  |
| minLength | Integer |  |
| regex | String |  |
| required | Boolean |  |
| sample | [SampleSchema](#SampleSchema) |  |
| type | String |  |
| ui | [PropertyUISchema](#PropertyUISchema) |  |
## [ModelDataTypeModelValidator](#ModelDataTypeModelValidator)

| property | type | documentation |
| --- | --- | --- |
| api-blueprint | [BlueprintSchema](#BlueprintSchema) | API blueprint details |
| config | [ConfigSchema](#ConfigSchema) | Application config details |
| enum | Array of Raw | A list of possible values |
| ext | [ExtSchema](#ExtSchema) | Application extension details |
| extend | String |  |
| json-schema-settings | [JSONSchema](#JSONSchema) | JSON Schema section of the model. Properties will be generated automatically |
| json-serializer | [JSONSerializerSchema](#JSONSerializerSchema) |  |
| mapping-settings | [ModelMappingSchema](#ModelMappingSchema) | Mapping definition |
| marshmallow | [ModelMarshmallowSchema](#ModelMarshmallowSchema) |  |
| model-name | String | Name of the model, will be used as module name if no module is specified |
| module | [ModuleSchema](#ModuleSchema) | Model module details |
| permissions | [ModelPermissionsSchema](#ModelPermissionsSchema) | Permissions settings |
| pid | [PIDSchema](#PIDSchema) | PID settings |
| properties | [ObjectPropertiesField](#ObjectPropertiesField) |  |
| proxy | [ProxySchema](#ProxySchema) | Settings for service proxy |
| record | [RecordClassSchema](#RecordClassSchema) | api/Record settings |
| record-dumper | [RecordDumperClassSchema](#RecordDumperClassSchema) | Settings for record dumper |
| record-metadata | [RecordMetadataClassSchema](#RecordMetadataClassSchema) | Record metadata settings |
| required | Boolean |  |
| resource | [ResourceClassSchema](#ResourceClassSchema) | Resource class settings |
| resource-config | [ResourceConfigClassSchema](#ResourceConfigClassSchema) | Resource config class settings |
| sample | [SampleSchema](#SampleSchema) | Settings for sample document generator |
| saved-model | [SavedModelSchema](#SavedModelSchema) |  |
| searchable | Boolean | Will the mapping/indexing be generated on model? (can be overriden on individual properties) |
| service | [ServiceClassSchema](#ServiceClassSchema) | Service settings |
| service-config | [ServiceConfigClassSchema](#ServiceConfigClassSchema) | Service config settings |
| type | String |  |
| ui | [ModelUISchema](#ModelUISchema) | UI settings |
| use | String |  |
## [ModelPermissionsSchema](#ModelPermissionsSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | Base classes for the generated permission class |
| class | String | Qualified name of the generated class |
| extra-code | String | Extra code to be copied below the permission class |
| generate | Boolean | Set to true to generate the permissions class |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | Module where the permissions will be placed |
| presets | Array of String | A list of presets that will be merged with the permissions class. |
## [ModelMarshmallowSchema](#ModelMarshmallowSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | List of marshmallow base classes |
| class | String | The name of the marshmallow class |
| extra-code | String | Extra code to be merged to marshmallow file |
| extra-fields | Array of [ExtraField](#ExtraField) | Extra fields to generate into the marhsmallow class |
| generate | Boolean | Generate the marshmallow class (default is true) |
| imports | Array of [ImportSchema](#ImportSchema) | Python imports that will be put to marshmallow file |
| module | String | Class module |
## [ModelUISchema](#ModelUISchema)

| property | type | documentation |
| --- | --- | --- |
| marshmallow | [ModelMarshmallowSchema](#ModelMarshmallowSchema) |  |
## [JSONSerializerSchema](#JSONSerializerSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | List of base classes |
| class | String | UI serializer class qualified name |
| extra-code | String | Extra code to be put below the generated ui serializer class |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | UI serializer class module |
## [ServiceClassSchema](#ServiceClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | List of base classes |
| class | String | Qualified name of the service class |
| config_key | String | Key under which actual service class is registered in config |
| extra-code | String | Extra code to be put below the generated service class |
| generate | Boolean | Generate service class (default) |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | Class module |
| proxy | String | name of the service proxy, will be put to _proxies_ package |
## [ServiceConfigClassSchema](#ServiceConfigClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | List of base classes |
| class | String | Qualified name of the service config class |
| components | Array of String | List of service components |
| config_key | String | Key under which the actual service config is registered in config |
| extra-code | String | Extra code to be put below the service config class |
| generate | Boolean | Generate the service config |
| generate-links | Boolean | Generate links section (default) |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | Class module |
| service-id | String | ID of the service |
## [RecordMetadataClassSchema](#RecordMetadataClassSchema)

| property | type | documentation |
| --- | --- | --- |
| alembic | String | module where alembic files are stored |
| alias | String | Alias under which the metadata is registered in setup.cfg |
| base-classes | Array of String | A list of base classes |
| class | String | Qualified name of the class |
| extra-code | String | Extra code to be put below the record |
| generate | Boolean | True to generate the metadata class |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | Module where the metadata class resides |
| table | String | Name of the database table |
## [RecordDumperClassSchema](#RecordDumperClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | List of base classes |
| class | String | Qualified name of the class |
| extensions | Array of String | List of dumper extensions |
| extra-code | String | Extra code to be copied to the bottom of the dumper file |
| generate | Boolean | Generate the dumper class |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | Class module |
## [PIDSchema](#PIDSchema)

| property | type | documentation |
| --- | --- | --- |
| context-class | String | Context class, PIDFieldContext is used if not passed |
| field-args | Array of String | Field arguments, default is create=True |
| field-class | String | Field class, PIDField is used if not passed in |
| generate | Boolean | Set to True (default) provider class |
| imports | Array of [ImportSchema](#ImportSchema) | A list of python imports |
| module | String | Module where the pid provider will be placed |
| provider-base-classes | Array of String | List of provider base classes |
| provider-class | String | Fully qualified name of the provider class |
| type | String | PID type, generated from model name if not passed |
## [ProxySchema](#ProxySchema)

| property | type | documentation |
| --- | --- | --- |
| module | String |  |
## [SavedModelSchema](#SavedModelSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Alias under which the model is registered in setup.cfg |
| file | String | File where to save the model |
| module | String | Module where the file is saved |
## [ResourceClassSchema](#ResourceClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | A list of base classes |
| class | String | Qualified name of the resource class |
| config_key | String | Name of the config entry that holds the current resource class name |
| extra-code | String | Extra code to be put to the bottom of the generated file |
| generate | Boolean | Generate the resource class (default) |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | Class module |
| proxy | String | name of the generated proxy, will be put to _proxies_ module |
## [ResourceConfigClassSchema](#ResourceConfigClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | A list of base classes |
| base-url | String | The base url of the resource |
| class | String | Qualified name of the config class |
| config_key | String | Name of the config entry that holds the current resource class name |
| extra-code | String | Extra code to be put below the generated config class |
| generate | Boolean | Generate the resource config class (default) |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | Class module |
## [RecordClassSchema](#RecordClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | Model base classes |
| class | String | Qualified name of the class |
| extra-code | String | Extra code to copy to record file |
| generate | Boolean | Set true to generate the class (default) |
| imports | Array of [ImportSchema](#ImportSchema) | List of python imports |
| module | String | Class module |
## [BlueprintSchema](#BlueprintSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Alias under which the blueprint will be registered in the setup.cfg |
| extra_code | String | Extra code to be pasted to blueprint |
| function | String | Fully qualified blueprint function |
| generate | Boolean | Generate blueprint, defaults to true |
| imports | Array of [ImportSchema](#ImportSchema) | Python imports |
| module | String | Module that will contain the blueprint |
## [ConfigSchema](#ConfigSchema)

| property | type | documentation |
| --- | --- | --- |
| extra_code | String | Extra code that will be pasted to app config |
| imports | Array of [ImportSchema](#ImportSchema) | Python imports |
| module | String | Module with app config |
## [ExtSchema](#ExtSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Alias under which the extension will be registered in setup.cfg and in app.extensions |
| base-classes | String | A list of extension's base classes |
| class | String | Extension class name |
| extra_code | String | Extra code that will be pasted to app extension module |
| imports | Array of [ImportSchema](#ImportSchema) | Python imports |
| module | String | Module with ext schema |
## [ModuleSchema](#ModuleSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Alias to use for setup.cfg etc. |
| base | String | Base name of the module (if the module has dot) |
| base-upper | String | Uppercase of the base name |
| kebab-module | String | Kebab case of the module |
| path | String | Path on the filesystem with the top-level module |
| prefix | String | Prefix that will be applied to class names |
| prefix_snake | String | Snake variant of the prefix |
| prefix_upper | String | Uppercase variant of the prefix |
| qualified | String | Module (fully qualified) where the model is generated |
| suffix | String | Suffix that will be applied to various names |
| suffix_snake | String | Snake variant of the suffix |
| suffix_upper | String | Uppercase variant of the suffix |
## [SampleSchema](#SampleSchema)

| property | type | documentation |
| --- | --- | --- |
| count | Integer | Number of generated records |
| file | String | File into which the records will be generated |
## [DefsSchema](#DefsSchema)

| property | type | documentation |
| --- | --- | --- |
## [SettingsSchema](#SettingsSchema)

| property | type | documentation |
| --- | --- | --- |
| opensearch | [SettingsOpenSearchSchema](#SettingsOpenSearchSchema) |  |
| python | [SettingsPythonSchema](#SettingsPythonSchema) |  |
| schema-server | String |  |
## [SettingsPythonSchema](#SettingsPythonSchema)

| property | type | documentation |
| --- | --- | --- |
| use-autoflake | Boolean |  |
| use-black | Boolean |  |
| use-isort | Boolean |  |
## [SettingsOpenSearchSchema](#SettingsOpenSearchSchema)

| property | type | documentation |
| --- | --- | --- |
| version | String |  |
