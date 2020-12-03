import enum


class OutputArch(enum.Enum):
    """Machine architecture"""

    X86_64 = enum.auto()
    I386 = enum.auto()
    NONE = enum.auto()

    def to_string(self) -> str:
        if self == OutputArch.X86_64:
            return "x86-64"
        elif self == OutputArch.I386:
            return "i386"
        else:
            return "NONE"