import importlib.resources as pkg_resources

from .. import builtin_models
import json

invenio = json.load(pkg_resources.open_text(builtin_models, 'invenio.json'))
