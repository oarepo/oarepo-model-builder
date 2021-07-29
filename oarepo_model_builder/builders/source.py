# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from typing import List

from oarepo_model_builder.builders import BuildResult
from oarepo_model_builder.builders import ElementBuilder


class SourceBuilder:
    """Base builder from source specification interface."""

    def walk(self, el, config, path, outputs, handlers) -> BuildResult:
        raise NotImplemented

    def __call__(self, *args, **kwargs):
        return self.walk(*args, **kwargs)

    def options(self):
        """returns list/tuple of click.argument or click.option options"""
        return ()


class DataModelBuilder(SourceBuilder):
    """Handles building a data model from a datamodel specification."""

    def walk(self, el, config, path, outputs, handlers: List[ElementBuilder] = None) -> BuildResult:
        """Walk the source data and call element handlers on each element."""
        if handlers is None:
            handlers = []

        result = BuildResult.KEEP
        for h in handlers:
            if h.pre(el, config, path, outputs) == BuildResult.DELETE:
                result = BuildResult.DELETE

        if isinstance(el, dict):
            for k, v in list(el.items()):
                if self.walk(v, config, path + [k], outputs, handlers) == BuildResult.DELETE:
                    del el[k]

        for h in handlers:
            h.post(el, config, path, outputs)

        return result
