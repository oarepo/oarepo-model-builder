import os

from munch import AutoMunch


class Config(AutoMunch):
    def resolve_path(self, relative_path, config_name=None):
        # if it is a config option and is set, return it (resolved to base_dir)
        if config_name and self.get(config_name, False):
            return os.path.join(self.base_dir, self[config_name])

        # otherwise construct it from relative path
        return os.path.join(self.base_dir, relative_path.format(**self))
