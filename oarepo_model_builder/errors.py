# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that generates data model files from a JSON specification file."""

import typing as t
from gettext import gettext as _

from click._compat import get_text_stderr
from click.exceptions import ClickException
from click.utils import echo


class BuildError(ClickException):
    exit_code = 10

    def show(self, file: t.Optional[t.IO] = None) -> None:
        if file is None:
            file = get_text_stderr()

        echo(_("Build Failed: {message}").format(message=self.format_message()), file=file)
