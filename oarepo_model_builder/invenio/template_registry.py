import pkg_resources


class TemplateRegistry:
    def __init__(self):
        # TODO: better loading, for example
        # print(pkgutil.get_data('oarepo_model_builder', 'invenio/templates/invenio_record.py.jinja2'))
        for ep in pkg_resources.iter_entry_points('oarepo_model_builder.templates1'):
            setattr(self, ep.name, ep.load())


templates = TemplateRegistry()
