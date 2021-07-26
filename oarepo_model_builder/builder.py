# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from enum import Enum
from typing import List

from oarepo_model_builder.output import MappingOutput


class WalkResult(Enum):
    KEEP = True
    DELETE = False


class BaseBuilder:
    """Base data model builder interface."""

    def pre(self, el, config, path, outputs):
        raise NotImplemented

    def walk(self, el, config, path, outputs, handlers) -> WalkResult:
        raise NotImplemented

    def post(self, el, config, path, outputs):
        raise NotImplemented

    def __call__(self, *args, **kwargs):
        raise NotImplemented


class DataModelBuilder(BaseBuilder):
    """Handles building a data model from a datamodel specification."""

    def walk(self, el, config, path, outputs, handlers: List[BaseBuilder] = None) -> WalkResult:
        """Walk the source data and call element handlers on each element."""
        if handlers is None:
            handlers = []

        results = []
        for h in handlers:
            results.append(h.pre(el, config, path, outputs))

        if isinstance(el, dict):
            for k, v in list(el.items()):
                if self.walk(v, outputs, path + [k], config, handlers) == WalkResult.DELETE:
                    del el[k]

        for h in handlers:
            h.post(el, config, path, outputs)

        return WalkResult.DELETE if any([r == WalkResult.DELETE for r in results]) else WalkResult.KEEP

    def __call__(self, *args, **kwargs):
        self.walk(*args, **kwargs)


class MappingBuilder(BaseBuilder):
    """Handles building of ES mappings from a data model specification."""

    def _resolve(self, el):
        if isinstance(el, str):
            # TODO: implement import of references here
            return dict(type=el)
        return el

    def pre(self, el, config, path, outputs):
        if not path:
            initial_data = config.get('mapping', {}).get('initial', None)
            outputs['mapping'] = MappingOutput(path=path, data=initial_data)
        elif path[-1] == 'search':
            # We are dealing with a field mapping, use path until 'properties' keyword as field path
            properties_idx = [i for i, j in enumerate(reversed(path[:-1])) if j == 'properties']
            if len(properties_idx) > 0:
                properties_idx = properties_idx[0]
            else:
                properties_idx = 0

            field_path = ['mappings'] + path[properties_idx:-1]
            outputs['mapping'].set(field_path, self._resolve(el))

            return WalkResult.DELETE

        return WalkResult.KEEP

    def post(self, el, config, path, outputs):
        pass
