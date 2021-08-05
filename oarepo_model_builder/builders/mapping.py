# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""

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
        if not search:
            return False
        if isinstance(search, dict) and 'mapping' in search:
            return self._resolve(search['mapping'])
        elif isinstance(search, str):
            return self._resolve(search)
        else:
            return self._resolve(self.default_type(config))

    def is_property(self, path):
        return len(path) > 1 and \
               path[-1] not in ['properties', 'mappings'] and \
               path[-2] == 'properties' and \
               path[0] == 'properties'

    def begin(self, config, outputs, root):
        output = outputs['mapping'] = MappingOutput()
        output.path = config.resolve_path(
            'mapping_path',
            'mappings/v7/{datamodel}-v{datamodel_version}.json')
        self.stack[0] = output.data
        if 'oarepo:search' in root:
            self.stack[-1].update(root['oarepo:search'])
        self.push({}, ['mappings'])

    def default_type(self, config):
        return config.search.get('default_mapping_type', 'keyword')

    def should_exclude(self, el, config):
        return el is False or \
               ('oarepo:search' in el and self._parse_oarepo_search(el['oarepo:search'], config) is False) or \
               ('oarepo:search' not in el and self.default_type(config) is False)

    def update_mapping_type(self, mapping_type='object'):
        """Sets a mapping type on first non-ignored element on stack"""
        for idx, entry in enumerate(reversed(self.stack)):
            if not self.should_ignore(entry):
                self.stack[-(idx + 1)]['type'] = mapping_type
                break

    def update_with_search(self, search, config):
        """Update first non-ignored element on stack with search configuration."""
        for idx, entry in enumerate(reversed(self.stack)):
            if not self.should_ignore(entry):
                search_config = self._parse_oarepo_search(search, config)
                if search_config is not False:
                    self.stack[-(idx + 1)].update(search_config)
                break

    def pre(self, el, config, path, outputs):
        if self.is_property(path):
            if self.should_exclude(el, config):
                self.push(self.IGNORED_SUBTREE, path)
                return

            # Map a concrete property to ES mapping
            self.push({}, path)
            if 'properties' in el:
                self.stack[-1]['type'] = 'object'
            else:
                self.stack[-1]['type'] = self.default_type(config)
        elif path[-1] == 'properties':
            # Map properties to ES mapping properties
            self.push({}, path)
        elif path[-1] == 'items':
            # Map array items to certain ES property mapping
            if 'properties' in el:
                if not self.should_exclude(el, config):
                    self.update_mapping_type()
                    self.push(self.IGNORED_NODE, path)
                else:
                    self.push(self.IGNORED_SUBTREE, path)
            elif 'oarepo:search' in el:
                self.update_with_search(el['oarepo:search'], config)
                self.push(self.IGNORED_SUBTREE, path)
            else:
                self.push(self.IGNORED_NODE, path)
        elif path[-1] == 'oarepo:search':
            # Update certain element with config from oarepo:search directive
            self.update_with_search(el, config)
            self.push(self.IGNORED_SUBTREE, path)
        elif path[0] != 'properties':
            # Ignore everything not starting with properties and not handled above
            self.push(self.IGNORED_SUBTREE, path)
        else:
            # Everything else is omitted from ES mapping output
            self.push(self.IGNORED_NODE, path)

    def post(self, el, config, path, outputs):
        self.pop()

    def end(self, config, outputs, root):
        self.pop()

    def options(self):
        return [
            click.option('mapping-path')
        ]
