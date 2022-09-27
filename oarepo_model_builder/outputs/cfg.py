from configupdater import ConfigUpdater, Option

from oarepo_model_builder.outputs import OutputBase


class CFGOutput(OutputBase):
    TYPE = "cfg"

    # high-level API

    def add_entry_point(self, group, name, value):
        """
        Adds an entry point if it is not already present
        """
        line = f"{name} = {value}"
        grp = self.create_multiline_value(
            "options.entry_points", group, initial_value=line
        )
        for e in grp.as_list():
            e = [x.strip() for x in e.split("=", maxsplit=1)]
            if len(e) == 2 and e[0] == name and e[1] == value:
                break
        else:
            grp.append(line)

    def add_dependency(
        self, package, version, group="options", section="install_requires", extras=None
    ):
        if extras:
            line = f'{package}[{", ".join(extras)}]{version}'
        else:
            line = f"{package}{version}"
        grp = self.create_multiline_value(group, section, line)
        for e in grp.as_list():
            if line == e.strip():
                break
        else:
            # TODO: this is a private api, but 'append' seems not to work on empty option
            grp.append(line)

    # low-level API

    def begin(self):
        try:
            with self.builder.filesystem.open(self.path) as f:
                self.original_data = f.read()
                self.cfg = ConfigUpdater()
                self.cfg.read_string(self.original_data)
                self.parsed = str(self.cfg)
        except FileNotFoundError:
            self.original_data = None
            self.cfg = ConfigUpdater()
            self.parsed = None

    @property
    def created(self):
        return self.original_data is None

    def get(self, section, key):
        try:
            tbl = self.cfg[section]
            return tbl[key]
        except KeyError:
            return None

    def get_section(self, section, create=False):
        if create and section not in self.cfg:
            self.cfg.add_section(section)
            tbl = self.cfg[section]
            tbl.add_before.space(2)
            return tbl
        return self.cfg[section]

    def set(self, section, key, value):
        tbl = self.get_section(section, create=True)
        tbl[key] = value

    def setdefault(self, section, key, value):
        tbl = self.get_section(section, create=True)
        return tbl.setdefault(key, value)

    def create_multiline_value(self, section, name, initial_value="") -> Option:
        tbl = self.get_section(section, create=True)
        if name in tbl:
            grp = tbl[name]
        else:
            grp = Option(name, value=initial_value)
            tbl.add_option(grp)
        return grp

    def finish(self):
        out = str(self.cfg)
        if out != self.parsed:
            with self.builder.filesystem.open(self.path, "w") as f:
                f.write(out)
