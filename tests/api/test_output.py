from oarepo_model_builder.outputs import BaseOutput


def test_base_output():
    bo = BaseOutput('', {'test': 'data'})

    assert bo.path == ''
    assert bo.output_type is None
    assert bo.data == {'test': 'data'}

    assert bo.data == {
        'test': 'data',
    }
