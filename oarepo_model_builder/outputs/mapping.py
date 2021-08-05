# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from copy import deepcopy

from oarepo_model_builder.outputs.json import JsonOutput
from oarepo_model_builder.proxies import current_model_builder


class MappingOutput(JsonOutput):
    """ES Mapping output."""
    output_type = 'mapping'

    def __init__(self, path=None, data=None):
        if data is None:
            data = deepcopy(current_model_builder.model_config.get('search').get('mapping', {}))

        super().__init__(path, data)
