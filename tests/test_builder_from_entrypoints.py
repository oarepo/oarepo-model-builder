import json
import os
import re

from oarepo_model_builder.entrypoints import load_model, create_builder_from_entrypoints
from tests.mock_open import MockOpen


def test_include_invenio():
    schema = load_model(
        'test.yaml', 'test',
        model_content={
            'model': {
                'oarepo:use': 'invenio',
                'properties': {
                    'a': {
                        'type': 'string'
                    }
                }
            }
        }, isort=False, black=False)

    open = MockOpen()
    builder = create_builder_from_entrypoints(open=open)

    builder.build(schema, '')

    data = builder.open(os.path.join('test', 'services', 'schema.py')).read()
    print(data)

    assert re.sub(r'\s', '', data) == re.sub(r'\s', '', """
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid

class TestSchema(ma.Schema, ):
    \"""TestSchema schema.\"""
    
    a = ma_fields.String()
    
    id = ma_fields.String()
    
    created = ma_fields.Date()
    
    updated = ma_fields.Date()
    
    _schema = ma_fields.String(attribute='$schema')
    
    uuid = ma_fields.String()    
    """)