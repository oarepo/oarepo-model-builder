# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
import json
from functools import cached_property
from typing import List

import pkg_resources

from oarepo_model_builder.builder import BaseBuilder


class _OARepoModelBuilderState:
    """OARepoModelBuilder extension state."""

    def __init__(self, app):
        self.app = app
        self._builders = None
        self._el_builders = None
        self._default_conf = None

    @property
    def datamodel_builders(self) -> List[BaseBuilder]:
        if self._builders is None:
            builders = []
            for entry_point in pkg_resources.iter_entry_points('oarepo_model_builder.datamodel'):
                builders.append(entry_point.load())
            builders.sort(key=lambda opener: -getattr(opener, '_priority', 10))
            self._builders = builders
        return self._builders

    @property
    def element_builders(self) -> List[BaseBuilder]:
        if self._el_builders is None:
            builders = []
            for entry_point in pkg_resources.iter_entry_points('oarepo_model_builder.elements'):
                builders.append(entry_point.load())
            builders.sort(key=lambda opener: -getattr(opener, '_priority', 10))
            self._el_builders = builders
        return self._el_builders

    @cached_property
    def model_config(self):
        if self._default_conf is None:
            try:
                import importlib.resources as pkg_resources
            except ImportError:
                # Try backported to PY<37 `importlib_resources`.
                import importlib_resources as pkg_resources

            from . import config
            config_json = pkg_resources.read_text(config, 'default.json')
            self._default_conf = json.loads(config_json)

            # TODO: iterate over oarepo_model_builder.config entrypoints and update

        return self._default_conf

    def output_builders(self, output_type) -> List[BaseBuilder]:
        builders = []
        for entry_point in pkg_resources.iter_entry_points(f'oarepo_model_builder.{output_type}'):
            builders.append(entry_point.load())
        builders.sort(key=lambda opener: -getattr(opener, '_priority', 10))
        return builders


class OARepoModelBuilder(object):
    """OARepoModelBuilder extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

        _state = _OARepoModelBuilderState(app)
        app.extensions['oarepo-model-builder'] = _state

    def init_config(self, app):
        """Initialize configuration."""
