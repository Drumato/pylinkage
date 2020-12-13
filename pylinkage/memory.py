from dataclasses import dataclass
from typing import Optional
import enum


class RegionAttr(enum.Enum):
    READONLY = enum.auto()
    READWRITE = enum.auto()
    EXECUTABLE = enum.auto()
    ALLOCATABLE = enum.auto()
    INITIALIZED = enum.auto()

    def to_string(self) -> str:
        if self == RegionAttr.READONLY:
            return "r"
        elif self == RegionAttr.READWRITE:
            return "w"
        elif self == RegionAttr.EXECUTABLE:
            return "x"
        elif self == RegionAttr.ALLOCATABLE:
            return "a"
        else:
            return "i"


class MemoryUnit(enum.Enum):
    KILO = enum.auto()
    MEGA = enum.auto()

    def to_string(self) -> str:
        if self == MemoryUnit.KILO:
            return "K"
        else:
            return "MEGA"


@dataclass
class RegionLength:
    length: int
    unit: MemoryUnit

    def to_string(self) -> str:
        return f"{self.length}{self.unit.to_string()}"


@dataclass
class Region:
    name: str
    attrs: Optional[list[RegionAttr]]
    origin: int
    length: RegionLength

    def to_ldscript(self) -> str:
        def attrs_to_str():
            if self.attrs is None:
                return ""
            return f'({"".join([a.to_string() for a in self.attrs])})'

        return f"{self.name} {attrs_to_str()}: ORIGIN = {hex(self.origin)}, LENGTH = {self.length.to_string()}"