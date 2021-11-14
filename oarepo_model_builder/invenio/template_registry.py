from pathlib import Path

import pkg_resources


class TemplateRegistry:
    def __init__(self):
        self.package_dirs = []
        for ep in sorted(
                pkg_resources.iter_entry_points('oarepo_model_builder.templates'),
                key=lambda ep: ep.name):
            self.package_dirs.append(Path(ep.load().__file__).parent)

    def __getattr__(self, item):
        for pd in self.package_dirs:
            item_path = pd.joinpath(item)
            # TODO: better loading, for data not present on the filesystem
            # print(pkgutil.get_data('oarepo_model_builder', 'invenio/templates/invenio_record.py.jinja2'))
            if item_path.exists():
                with item_path.open() as f:
                    return f.read()
        raise AttributeError(f'Template with name {item} has not been found')


templates = TemplateRegistry()
