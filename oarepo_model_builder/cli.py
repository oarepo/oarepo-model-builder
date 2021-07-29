# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""
import os

import click
import json5
from flask.cli import with_appcontext

from oarepo_model_builder.api import build_datamodel
from oarepo_model_builder.proxies import current_model_builder


@click.group()
def model():
    """Management commands for OARepo Model Builder."""
    pass


@model.command('build')
@click.argument('source', type=click.Path(readable=True, exists=True))
@with_appcontext
def build(source, base_dir=os.getcwd()):
    """Build data model files from JSON5 source specification."""
    click.secho('Generating models from: ' + source, fg='green')
    with open(source) as datamodel_file:
        data = json5.load(datamodel_file)

    build_datamodel(data, config=current_model_builder.model_config)
