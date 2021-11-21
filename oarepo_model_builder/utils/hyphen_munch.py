from typing import Mapping

import munch


class HyphenMunch(munch.AutoMunch):
    def __setitem__(self, key, value):
        key = key.replace('_', '-')
        if isinstance(value, Mapping) and not isinstance(value, (munch.AutoMunch, munch.Munch)):
            value = munch.munchify(value, HyphenMunch)
        return super().__setitem__(key, value)

    def __getitem__(self, key):
        key = key.replace('_', '-')
        return super().__getitem__(key)