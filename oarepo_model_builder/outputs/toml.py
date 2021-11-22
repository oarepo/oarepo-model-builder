from tomlkit.exceptions import NonExistentKey

from oarepo_model_builder.outputs import OutputBase
import tomlkit


class TOMLOutput(OutputBase):
    TYPE = 'toml'

    def begin(self):
        try:
            with self.builder.open(self.path) as f:
                self.original_data = f.read()
                self.toml = tomlkit.parse(self.original_data)
                self.parsed = tomlkit.dumps(self.toml, sort_keys=True)
        except FileNotFoundError:
            self.original_data = None
            self.toml = tomlkit.document()
            self.parsed = None

    def table(self, key):
        try:
            return self.toml.item(key)
        except NonExistentKey:
            t = tomlkit.table()
            self.toml.append(key, t)
            return t

    def get(self, table, key):
        try:
            tbl = self.toml.item(table)
            return tbl.item(key)
        except NonExistentKey:
            return None

    def set(self, table, key, value):
        tbl = self.table(table)
        tbl[key] = value

    def finish(self):
        out = tomlkit.dumps(self.toml, sort_keys=True)
        if out != self.parsed:
            with self.builder.open(self.path, 'w') as f:
                f.write(tomlkit.dumps(self.toml))
