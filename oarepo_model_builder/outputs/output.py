# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
import json
import os

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

    def __init__(self, path=None, data=None):
        self.path = path
        self._data = data

    def save(self):
        raise NotImplemented

    @property
    def data(self):
        return self._data

    def __call__(self, *args, **kwargs):
        pass


class JsonOutput(BaseOutput):
    """Output that handles JSON formatted data."""

    def save(self):
        if self.data and self.path:
            parent = os.path.dirname(self.path)
            if not os.path.exists(parent):
                os.makedirs(parent)
                # TODO: maybe add __init__.py automatically into each created dir?
            with open(self.path, mode='w') as fp:
                fp.write(json.dumps(self.data))
