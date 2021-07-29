# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""

from oarepo_model_builder.outputs.output import BaseOutput


class UIOutput(BaseOutput):
    output_type = 'ui'

    def __init__(self, path):
        super().__init__(path, {})
