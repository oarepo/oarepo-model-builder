# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from deepmerge import Merger

_output_merger = Merger(
    [
        (list, ["append"]),
        (dict, ["merge"]),
        (set, ["union"])
    ],
    ["override"],
    ["override"]
)


class BaseOutput:
    """Base output handler interface."""
    output_type = None

    def __init__(self, path, data=None):
        self.path = path
        self._data = data

    def save(self):
        raise NotImplemented

    def set(self, path, val):
        def _unflatten(paths, data):
            _path = paths[0]
            data.setdefault(_path, {})

            if len(paths) == 1:
                data[_path] = val
            else:
                _unflatten(paths[1:], data[_path])

        d = {}
        _unflatten(path, d)

        print(d)

        self._data = _output_merger.merge(self._data, dict(d))

    @property
    def data(self):
        return self._data

    def __call__(self, *args, **kwargs):
        raise NotImplemented
