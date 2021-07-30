import os

from munch import AutoMunch


class Config(AutoMunch):
    def resolve_path(self, config_name, default_path=None):
        # if it is a config option and is set, return it (resolved to base_dir)
        if config_name and self.get(config_name, False):
            return os.path.join(self.base_dir, self[config_name])

        if default_path is None:
            raise AttributeError(f'Config "{config_name}" is not set')

        # otherwise construct it from default path
        return os.path.join(self.base_dir, default_path.format(**self))
