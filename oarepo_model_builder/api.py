# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
from copy import deepcopy
from typing import Dict

from deepmerge import Merger

from oarepo_model_builder.output import BaseOutput
from oarepo_model_builder.proxies import current_model_builder

_includes_merger = Merger(
    [
        (list, ["append"]),
        (dict, ["merge"]),
        (set, ["union"])
    ],
    ["override"],
    ["override"]
)


def resolve_includes(src, prop):
    if isinstance(src, dict):
        while 'oarepo:type' in src:
            includes = src.pop('oarepo:type')
            if not isinstance(includes, (list, tuple)):
                included_datamodel = deepcopy(current_model_builder.datamodels[includes])

            elif includes:
                included_datamodel = {}

                for inc in includes:
                    _includes_merger.merge(included_datamodel,
                                           deepcopy(current_model_builder.datamodels[inc]))
            else:
                included_datamodel = {}

            _includes_merger.merge(included_datamodel, src)
            src.update(included_datamodel)

        if prop == 'properties':
            for k, v in list(src.items()):
                if isinstance(v, (str, list, tuple)):
                    src[k] = {'oarepo:type': v}
                elif isinstance(v, dict) and 'items' in v and isinstance(v['items'], (str, list, tuple)):
                    v['items'] = {'oarepo:type': v['items']}

        for k, v in list(src.items()):
            if k == 'properties' and isinstance(v, (str, list, tuple)):
                src[k] = {'oarepo:type': v}

            resolve_includes(v, k)

    elif isinstance(src, (list, tuple)):
        for v in src:
            resolve_includes(v, prop)


def build_datamodel_files(src, config=None):
    """Build data model files from source JSON5 specification data."""
    if config is None:
        config = {}

    outputs: Dict[str: BaseOutput] = {}

    # Resolve includes
    resolve_includes(src, None)

    # Iterate over registered model builders
    for builder in current_model_builder.datamodel_builders:
        el_handlers = current_model_builder.element_builders

        builder(el=src, config=config, path=[], outputs=outputs, handlers=el_handlers)

        for output_name, output in list(outputs.items()):
            out_handlers = current_model_builder.output_builders(output.output_type)
            for oh in out_handlers:
                oh(output.data, config, output.path, outputs)

    for output in outputs.values():
        output.save()
