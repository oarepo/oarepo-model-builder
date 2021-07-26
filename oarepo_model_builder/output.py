# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from collections import defaultdict
from enum import Enum
from functools import reduce
from operator import getitem
from typing import List

from oarepo_model_builder.proxies import current_model_builder


class BaseOutput:
    """Base output handler interface."""
    output_type = None

    def __init__(self, path, data=None):
        self.path = path
        self._data = data

    def save(self):
        raise NotImplemented

    def set(self, path, val):
        def _default():
            return defaultdict(_default)

        def _defaultify(d):
            if not isinstance(d, dict):
                return d
            return defaultdict(_default, {k: _defaultify(v) for k, v in d.items()})

        data = _defaultify(self._data)
        reduce(getitem, path[:-1], data)[path[-1]] = val

        self._data = data

    @property
    def data(self):
        return self._data

    def __call__(self, *args, **kwargs):
        raise NotImplemented


class MappingOutput(BaseOutput):
    """ES Mapping output."""
    output_type = 'mapping'

    def __init__(self, path, data=None):
        if data is None:
            data = current_model_builder.model_config.get('search').get('mapping')

        super().__init__(path, data)


class JsonSchemaOutput(BaseOutput):
    """Output class for jsonschema."""
    output_type = 'jsonschema'

    def __init__(self, path, data=None):
        if data is None:
            data = current_model_builder.model_config.get('jsonschema')

        super().__init__(path, data)
