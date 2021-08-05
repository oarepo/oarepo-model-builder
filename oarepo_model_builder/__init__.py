# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""OArepo module that generates data model files from a JSON specification file."""

import os
from copy import deepcopy
from functools import cached_property

import json5
import pkg_resources

from oarepo_model_builder.config import Config
from oarepo_model_builder.errors import BuildError


class OARepoModelBuilder:
    """OARepoModelBuilder extension state."""

    def __init__(self):
        self._builders = None
        self._el_builders = None
        self._default_conf = None

    @cached_property
    def datamodels(self):
        models = {}
        for entry_point in pkg_resources.iter_entry_points('oarepo_model_builder.datamodels'):
            ep = entry_point.load()
            directory = os.path.dirname(ep.__file__)
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)

                if file.lower().endswith(('.json5', '.json')):
                    model_name = file.rsplit('.', 1)[0]
                    with open(file_path) as mf:
                        models[model_name] = json5.load(mf)

        return models

    def get_model(self, name):
        try:
            return deepcopy(self.datamodels[name])
        except KeyError:
            raise BuildError(f'datamodel "{name}" not in registered datamodels')

    @property
    def source_builders(self) -> list:
        if self._builders is None:
            builders = []
            for entry_point in pkg_resources.iter_entry_points('oarepo_model_builder.source'):
                cls = entry_point.load()
                builders.append(cls())
            builders.sort(key=lambda opener: -getattr(opener, '_priority', 10))
            self._builders = builders
        return self._builders

    @property
    def element_builders(self) -> list:
        if self._el_builders is None:
            builders = []
            for entry_point in pkg_resources.iter_entry_points('oarepo_model_builder.elements'):
                cls = entry_point.load()
                builders.append(cls())
            builders.sort(key=lambda opener: -getattr(opener, '_priority', 10))
            self._el_builders = builders
        return self._el_builders

    @cached_property
    def model_config(self):
        try:
            import importlib.resources as resources
        except ImportError:
            # Try backported to PY<37 `importlib_resources`.
            import importlib_resources as resources

        from . import config
        config_json = resources.read_text(config, 'default.json')
        return Config(json5.loads(config_json))

    def output_builders(self, output_type) -> list:
        builders = []
        for entry_point in pkg_resources.iter_entry_points(f'oarepo_model_builder.{output_type}'):
            cls = entry_point.load()
            builders.append(cls())
        builders.sort(key=lambda opener: -getattr(opener, '_priority', 10))
        return builders
