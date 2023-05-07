## [ModelFileSchema](#ModelFileSchema)

| property | type | documentation |
| --- | --- | --- |
| $defs | [DefsSchema](#DefsSchema) | Extra definitions, might be included via _use_ or _extend_ |
| output-directory | String | Directory where sources will be generated to |
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
| json-schema | [JSONSchema](#JSONSchema) | JSON Schema section of the model. Properties will be generated automatically |
| mapping | [ModelMappingSchema](#ModelMappingSchema) | Mapping definition |
| marshmallow | [ModelMarshmallowSchema](#ModelMarshmallowSchema) |  |
| model-name | String | Name of the model, will be used as package name if no package is specified |
| package | [PackageSchema](#PackageSchema) | Model package details |
| permissions | [ModelPermissionsSchema](#ModelPermissionsSchema) |  |
| pid | [PIDSchema](#PIDSchema) |  |
| profile-name | String | Actual profile |
| properties | [ObjectPropertiesField](#ObjectPropertiesField) |  |
| record | [RecordClassSchema](#RecordClassSchema) |  |
| record-dumper | [RecordDumperClassSchema](#RecordDumperClassSchema) |  |
| record-metadata | [RecordMetadataClassSchema](#RecordMetadataClassSchema) |  |
| record-ui-serializer-class | String |  |
| required | Boolean |  |
| resource | [ResourceClassSchema](#ResourceClassSchema) |  |
| resource-config | [ResourceConfigClassSchema](#ResourceConfigClassSchema) |  |
| sample | [SampleSchema](#SampleSchema) |  |
| saved-model | [SavedModelSchema](#SavedModelSchema) |  |
| service | [ServiceClassSchema](#ServiceClassSchema) |  |
| service-config | [ServiceConfigClassSchema](#ServiceConfigClassSchema) |  |
| type | String |  |
| ui | [ObjectUIExtraSchema](#ObjectUIExtraSchema) |  |
| ui-blueprint | [BlueprintSchema](#BlueprintSchema) | UI blueprint details |
| use | String |  |
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
| extend | String |  |
| extra-fields | Array of [ExtraField](#ExtraField) | Extra fields to generate into the marhsmallow class |
| field | String |  |
| field-class | String |  |
| field-name | String |  |
| generate | Boolean | Generate the marshmallow class (default is true) |
| imports | Array of [ImportSchema](#ImportSchema) |  |
| read | Boolean |  |
| schema-class | String | The name of the marshmallow class |
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
| json-schema | [JSONSchema](#JSONSchema) | JSON Schema section of the model. Properties will be generated automatically |
| mapping | [ModelMappingSchema](#ModelMappingSchema) | Mapping definition |
| marshmallow | [ModelMarshmallowSchema](#ModelMarshmallowSchema) |  |
| model-name | String | Name of the model, will be used as package name if no package is specified |
| package | [PackageSchema](#PackageSchema) | Model package details |
| permissions | [ModelPermissionsSchema](#ModelPermissionsSchema) |  |
| pid | [PIDSchema](#PIDSchema) |  |
| profile-name | String | Actual profile |
| properties | [ObjectPropertiesField](#ObjectPropertiesField) |  |
| record | [RecordClassSchema](#RecordClassSchema) |  |
| record-dumper | [RecordDumperClassSchema](#RecordDumperClassSchema) |  |
| record-metadata | [RecordMetadataClassSchema](#RecordMetadataClassSchema) |  |
| record-ui-serializer-class | String |  |
| required | Boolean |  |
| resource | [ResourceClassSchema](#ResourceClassSchema) |  |
| resource-config | [ResourceConfigClassSchema](#ResourceConfigClassSchema) |  |
| sample | [SampleSchema](#SampleSchema) |  |
| saved-model | [SavedModelSchema](#SavedModelSchema) |  |
| service | [ServiceClassSchema](#ServiceClassSchema) |  |
| service-config | [ServiceConfigClassSchema](#ServiceConfigClassSchema) |  |
| type | String |  |
| ui | [ObjectUIExtraSchema](#ObjectUIExtraSchema) |  |
| ui-blueprint | [BlueprintSchema](#BlueprintSchema) | UI blueprint details |
| use | String |  |
## [PackageSchema](#PackageSchema)

| property | type | documentation |
| --- | --- | --- |
## [ObjectUIExtraSchema](#ObjectUIExtraSchema)

| property | type | documentation |
| --- | --- | --- |
| marshmallow | [ObjectMarshmallowSchema](#ObjectMarshmallowSchema) |  |
## [ServiceClassSchema](#ServiceClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String |  |
| class | String |  |
| config_key | String |  |
| extra-code | String |  |
| generate | Boolean |  |
| proxy | String |  |
## [ServiceConfigClassSchema](#ServiceConfigClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String |  |
| class | String |  |
| components | Array of String |  |
| config_key | String |  |
| extra-code | String |  |
| generate | Boolean |  |
| generate-links | Boolean |  |
| service-id | String |  |
## [SavedModelSchema](#SavedModelSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String |  |
| file | String |  |
## [SampleSchema](#SampleSchema)

| property | type | documentation |
| --- | --- | --- |
| count | Integer |  |
## [ResourceClassSchema](#ResourceClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String |  |
| class | String |  |
| config_key | String |  |
| extra-code | String |  |
| generate | Boolean |  |
| proxy | String |  |
## [ResourceConfigClassSchema](#ResourceConfigClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String |  |
| base-url | String |  |
| class | String |  |
| config_key | String |  |
| extra-code | String |  |
| generate | Boolean |  |
## [RecordClassSchema](#RecordClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String |  |
| class | String |  |
| extra-code | String |  |
| generate | Boolean |  |
| package | String |  |
## [RecordMetadataClassSchema](#RecordMetadataClassSchema)

| property | type | documentation |
| --- | --- | --- |
| alembic | String |  |
| alias | String |  |
| base-classes | Array of String |  |
| class | String |  |
| extra-code | String |  |
| generate | Boolean |  |
| package | String |  |
| table | String |  |
## [RecordDumperClassSchema](#RecordDumperClassSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String |  |
| class | String |  |
| extensions | Array of String |  |
| extra-code | String |  |
| generate | Boolean |  |
## [ModelPermissionsSchema](#ModelPermissionsSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String |  |
| class | String |  |
| extra-code | String |  |
| generate | Boolean |  |
| presets | Array of String |  |
## [PIDSchema](#PIDSchema)

| property | type | documentation |
| --- | --- | --- |
| context-class | String |  |
| field-args | Array of String |  |
| field-class | String |  |
| generate | Boolean |  |
| imports | Array of [ImportSchema](#ImportSchema) |  |
| provider-base-classes | Array of String |  |
| provider-class | String |  |
| type | String |  |
## [ModelMarshmallowSchema](#ModelMarshmallowSchema)

| property | type | documentation |
| --- | --- | --- |
| base-classes | Array of String | List of marshmallow base classes |
| extra-code | String | Extra code to be merged to marshmallow file |
| extra-fields | Array of [ExtraField](#ExtraField) | Extra fields to generate into the marhsmallow class |
| generate | Boolean | Generate the marshmallow class (default is true) |
| imports | Array of [ImportSchema](#ImportSchema) | Python imports that will be put to marshmallow file |
| schema-class | String | The name of the marshmallow class |
## [ModelMappingSchema](#ModelMappingSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Index alias, under which the mapping is registered in setup.cfg |
| file | String | Path to index file |
| index | String | Index name |
| template | [PermissiveSchema](#PermissiveSchema) | Mapping template, merged with generated mapping |
## [PermissiveSchema](#PermissiveSchema)

| property | type | documentation |
| --- | --- | --- |
| extend | String |  |
| use | String |  |
## [JSONSchema](#JSONSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Alias under which jsonschema is referenced in setup.cfg |
| file | String | Path to schema file |
| name | String | Schema name |
| template | [PermissiveSchema](#PermissiveSchema) | Template that will be merged with the schema |
| version | String | Schema version |
## [BlueprintSchema](#BlueprintSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Alias under which the blueprint will be registered in the setup.cfg |
| extra_code | String | Extra code to be pasted to blueprint |
| function | String | Fully qualified blueprint function |
## [ConfigSchema](#ConfigSchema)

| property | type | documentation |
| --- | --- | --- |
| extra_code | String | Extra code that will be pasted to app config |
| package | String | Package with app config |
## [ExtSchema](#ExtSchema)

| property | type | documentation |
| --- | --- | --- |
| alias | String | Alias under which the extension will be registered in setup.cfg |
| base-classes | String | A list of extension's base classes |
| class | String | Extension class name |
| extra_code | String | Extra code that will be pasted to app extension module |
## [DefsSchema](#DefsSchema)

| property | type | documentation |
| --- | --- | --- |
## [SettingsSchema](#SettingsSchema)

| property | type | documentation |
| --- | --- | --- |
| opensearch | [SettingsOpenSearchSchema](#SettingsOpenSearchSchema) |  |
| python | [SettingsPythonSchema](#SettingsPythonSchema) |  |
| schema-version | String |  |
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
