# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from typing import Dict

from oarepo_model_builder.output import BaseOutput
from oarepo_model_builder.proxies import current_model_builder


def build_datamodel_files(src, config=None):
    """Build data model files from source JSON5 specification data."""
    if config is None:
        config = {}

    outputs: Dict[str: BaseOutput] = {}

    for builder in current_model_builder.datamodel_builders:
        el_handlers = current_model_builder.element_builders

        builder(el=src, config=config, path=[], outputs=outputs, handlers=el_handlers)

        for output_name, output in list(outputs.items()):
            out_handlers = current_model_builder.output_builders(output.output_type)
            for oh in out_handlers:
                oh(output.data, config, output.path, outputs)

    for output in outputs.values():
        output.save()
