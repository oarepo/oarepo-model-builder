# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
import copy

import click

from oarepo_model_builder.builders import JSONBuilder
from oarepo_model_builder.outputs import MappingOutput


class MappingBuilder(JSONBuilder):
    """Handles building of ES mappings from source elements."""

    def _resolve(self, el):
        if isinstance(el, str):
            return dict(type=el)
        return el

    def _parse_oarepo_search(self, search, config):
        if isinstance(search, dict) and 'mapping' in search:
            return self._resolve(search['mapping'])
        elif isinstance(search, str):
            return self._resolve(search)
        else:
            return self._resolve(self.default_type(config))

    def is_property(self, path):
        return len(path) > 1 and path[-2] == 'properties'  # TODO: tohle neni uplne spravne

    def begin(self, config, outputs, root):
        output = outputs['mapping'] = MappingOutput(path=config.resolve_path(
            'mapping_path',
            'mappings/v7/{datamodel}-v{datamodel_version}.json'))
        self.stack[0] = output.data
        if 'oarepo:search' in root:
            self.stack[-1].update(root['oarepo:search'])
        self.push({}, ['mappings'])

    def default_type(self, config):
        return config.search.get('default_mapping_type', 'keyword')

    def pre(self, el, config, path, outputs):
        if self.is_property(path):
            self.push({}, path)

            if 'properties' in el:
                self.stack[-1]['type'] = 'object'
            else:
                self.stack[-1]['type'] = self.default_type(config)

        elif path[-1] == 'properties':
            self.push({}, path)
        elif path[-1] == 'items':
            if 'properties' in el:
                self.stack[-1]['type'] = 'object'
                self.push(self.IGNORED_NODE, path)
            elif 'oarepo:search' in el:
                self.stack[-1].update(self._parse_oarepo_search(el['oarepo:search'], config))
                self.push(self.IGNORED_SUBTREE, path)
            else:
                self.push(self.IGNORED_NODE, path)
        elif path[-1] == 'oarepo:search' and self.stack[-1] is not self.IGNORED_SUBTREE:
            self.stack[-1].update(self._parse_oarepo_search(el, config))
            self.push(self.IGNORED_SUBTREE, path)
        else:
            self.push(self.IGNORED_NODE, path)

    def post(self, el, config, path, outputs):
        self.pop()

    def end(self, config, outputs, root):
        self.pop()

    def options(self):
        return [
            click.option('mapping-path')
        ]
