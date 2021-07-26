from oarepo_model_builder import __version__

from flask import Flask

from oarepo_model_builder.ext import OARepoModelBuilder


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = OARepoModelBuilder(app)
    assert 'oarepo-model-builder' in app.extensions

    app = Flask('testapp')
    ext = OARepoModelBuilder()
    assert 'oarepo-model-builder' not in app.extensions
    ext.init_app(app)
    assert 'oarepo-model-builder' in app.extensions


def test_version():
    assert __version__ == '0.1.0'
