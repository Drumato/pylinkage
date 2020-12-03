from __future__ import annotations
import enum

"""
GNU ld's supporing targets
elf64-x86-64 elf32-i386 elf32-iamcu elf32-x86-64 pei-i386 pei-x86-64 elf64-l1om elf64-k1om elf64-little elf64-big elf32-little elf32-big pe-x86-64 pe-bigobj-x86-64 pe-i386 srec symbolsrec verilog tekhex binary ihex plugin
"""


class OutputFormat(enum.Enum):
    """Object file format"""

    ELF64_X86_64 = enum.auto()
    ELF32_I386 = enum.auto()
    BINARY = enum.auto()
    NONE = enum.auto()

    def to_string(self) -> str:
        if self == OutputFormat.ELF64_X86_64:
            return "elf64-x86-64"
        elif self == OutputFormat.ELF32_I386:
            return "elf32-i386"
        elif self == OutputFormat.BINARY:
            return "binary"
        else:
            return "NONE"