# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""


class ElementBuilder:
    """Base element builder interface."""

    def begin(self, config, outputs, root):
        pass

    def end(self, config, outputs, root):
        pass

    def pre(self, el, config, path, outputs):
        raise NotImplemented

    def post(self, el, config, path, outputs):
        raise NotImplemented

    def options(self):
        """returns list/tuple of click.argument or click.option options"""
        return ()
