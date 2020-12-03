from __future__ import annotations

from dataclasses import dataclass, field
import sys


@dataclass
class PyLinkageError:
    msg: str = field(default="")

    def not_found_such_an_attribute(self, attribute_name: str) -> PyLinkageError:
        self.msg = f"Not found such an attribute => '{attribute_name}'"
        return self

    def emit(self):
        sys.stderr.write(self.msg)