# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from typing import List

from oarepo_model_builder.outputs.output import BaseOutput


class OutputBuilder:
    """Base output files builder interface."""

    def save(self, *args, **kwargs):
        raise NotImplemented

    def __call__(self, data, config, path, outputs: List[BaseOutput]):
        raise NotImplemented
