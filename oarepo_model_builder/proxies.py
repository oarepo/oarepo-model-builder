# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""

from flask import current_app
from werkzeug.local import LocalProxy

current_model_builder = LocalProxy(lambda: current_app.extensions['oarepo-model-builder'])
