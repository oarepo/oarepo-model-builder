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
