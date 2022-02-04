from typing import Optional

from faker.providers import BaseProvider


class Provider(BaseProvider):
    def sentence(self):
        return "test"

    def random_int(self, min: int = 0, max: int = 9999, step: int = 1) -> int:
        return 1

    def random_float(self, digits: Optional[int] = None, fix_len: bool = False) -> int:
        return 1.2

    def date(self):
        return "2022-01-02"
