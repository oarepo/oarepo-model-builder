from pathlib import Path

from oarepo_model_builder.builders import OutputBuilder

from ..utils.dict import dict_get
from .utils import ensure_parent_modules


class JSONBaseBuilder(OutputBuilder):
    output_file_name: str
    output_file_type: str
    parent_module_root_name = None
    create_parent_packages = False

    def begin(self, current_model, schema):
        super().begin(current_model, schema)
        output_name = dict_get(self.current_model.definition, self.output_file_name)
        self.output = self.builder.get_output(self.output_file_type, output_name)

        if self.create_parent_packages:
            package_path = Path(output_name).parent
            ensure_parent_modules(
                self.builder,
                self.builder.output_dir.joinpath(package_path / "__init__.py"),
                max_depth=len(package_path.parts),
            )

    def finish(self):
        return super().finish()
