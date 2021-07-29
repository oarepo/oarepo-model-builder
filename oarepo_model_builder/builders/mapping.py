# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from copy import deepcopy

from oarepo_model_builder.builders import JSONBuilder
from oarepo_model_builder.builders import BuildResult
from oarepo_model_builder.outputs import MappingOutput


class MappingBuilder(JSONBuilder):
    """Handles building of ES mappings from source elements."""

    def _resolve(self, el):
        if isinstance(el, str):
            # TODO: implement import of references here
            return dict(type=el)
        return el

    def pre(self, el, config, path, outputs):
        if not path:
            initial_data = deepcopy(config.get('mapping', {}).get('initial', None))
            outputs['mapping'] = MappingOutput(path=path, data=initial_data)
        elif path[-1] == 'search':
            # We are dealing with a field mapping, use path until 'properties' keyword as field path
            properties_idx = [i for i, j in enumerate(reversed(path[:-1])) if j == 'properties']
            if len(properties_idx) > 0:
                properties_idx = min(properties_idx[0] - 1, 0)
            else:
                properties_idx = 0

            field_path = ['mappings'] + path[properties_idx:-1]
            outputs['mapping'].set(field_path, self._resolve(el))
            return BuildResult.DELETE

        return BuildResult.KEEP

    def post(self, el, config, path, outputs):
        pass
