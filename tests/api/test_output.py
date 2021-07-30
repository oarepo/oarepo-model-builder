from oarepo_model_builder.outputs import BaseOutput


def test_base_output():
    bo = BaseOutput('', {'test': 'data'})

    assert bo.path == ''
    assert bo.output_type is None
    assert bo.data == {'test': 'data'}

    bo.set(['testpath', 'subpath', 'subsub'], 'test1')
    bo.set(['testpath', 'subpath', 'subsub2'], 'test2')

    assert bo.data == {
        'test': 'data',
        'testpath': {
            'subpath': {
                'subsub': 'test1',
                'subsub2': 'test2'
            }
        }
    }
