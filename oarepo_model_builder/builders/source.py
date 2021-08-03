# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from typing import List

from oarepo_model_builder.builders import ElementBuilder


class SourceBuilder:
    """Base builder from source specification interface."""

    def walk(self, el, config, path, outputs, handlers):
        raise NotImplemented

    def __call__(self, el, config, path, outputs, handlers, *args, **kwargs):
        for h in handlers:
            h.begin(config, outputs, el)

        self.walk(el, config, path, outputs, handlers, *args, **kwargs)

        for h in handlers:
            h.end(config, outputs, el)

    def options(self):
        """returns list/tuple of click.argument or click.option options"""
        return ()


class DataModelBuilder(SourceBuilder):
    """Handles building a data model from a datamodel specification."""

    def walk(self, el, config, path, outputs, handlers: List[ElementBuilder] = None):
        """Walk the source data and call element handlers on each element."""
        if handlers is None:
            handlers = []

        if path:
            for h in handlers:
                h.pre(el, config, path, outputs)

        if isinstance(el, dict):
            for k, v in list(el.items()):
                self.walk(v, config, path + [k], outputs, handlers)

        if path:
            for h in handlers:
                h.post(el, config, path, outputs)
