from __future__ import annotations
import enum


class OutputMode(enum.Enum):
    YAML = enum.auto()
    SCRIPT = enum.auto()
    NONE = enum.auto()