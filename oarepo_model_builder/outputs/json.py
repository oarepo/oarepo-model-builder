# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
import json
import os

from oarepo_model_builder.outputs.output import BaseOutput


class JsonOutput(BaseOutput):
    """Output that handles JSON formatted data."""

    def save(self):
        if self.data and self.path:
            parent = os.path.dirname(self.path)
            if not os.path.exists(parent):
                os.makedirs(parent)
                # TODO: maybe add __init__.py automatically into each created dir?
            with open(self.path, mode='w') as fp:
                fp.write(json.dumps(self.data, indent=2, sort_keys=True))
