# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
import functools
import os

import click
import json5

from oarepo_model_builder.api import build_datamodel
from oarepo_model_builder.proxies import current_model_builder


@click.group()
def model():
    """Management commands for OARepo Model Builder."""
    pass


def builder_arguments(f):
    args = []
    # TODO: gather arguments from source and element builders when current_model_builder is a singleton
    # TODO: can not be called now as it requires app_context that is not yet existing
    #
    # for builder in current_model_builder.source_builders:
    #     args.extend(builder.options())
    # for builder in current_model_builder.element_builders:
    #     args.extend(builder.options())
    for arg in args:
        f = functools.wraps(f)(arg(f))
    return f


@model.command('build')
@click.argument('source', type=click.Path(readable=True, exists=True))
@click.option('--package')
@click.option('--config-path', '-c', type=click.Path(readable=True, exists=True))
@click.option('--datamodel-version', default='1.0.0')
@builder_arguments
def build(source, base_dir=os.getcwd(), config_path=None, **kwargs):
    """Build data model files from JSON5 source specification."""
    click.secho('Generating models from: ' + source, fg='green')
    with open(source) as datamodel_file:
        data = json5.load(datamodel_file)

    config = current_model_builder.model_config

    if config_path:
        with open(config_path) as config_file:
            config.update(json5.load(config_file))

    config.update(kwargs)      # config is an instance of Munch, so can use either dict or dot style
    config.source = source
    config.base_dir = base_dir
    config.package = kwargs['package'] or (os.path.basename(os.getcwd())).replace('-', '_')
    config.kebab_package = config.package.replace('_', '-')
    config.datamodel = config.kebab_package
    build_datamodel(data, config=config)
