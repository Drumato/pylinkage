import pylinkage as pyl


def test_output_format_to_ldscript():
    generator = pyl.ScriptGenerator()
    generator.object_format = pyl.OutputFormat.ELF64_X86_64
    fmt_string = generator._ScriptGenerator__output_format_to_ldscript()
    assert fmt_string == "OUTPUT_FORMAT(elf64-x86-64)"

    # check how its failure
    delattr(generator, "object_format")
    fmt_string = generator._ScriptGenerator__output_format_to_ldscript()
    assert fmt_string == pyl.PyLinkageError(
        msg="Not found such an attribute => 'object_format'"
    )


def test_output_arch_to_ldscript():
    generator = pyl.ScriptGenerator()
    generator.architecture = pyl.OutputArch.I386
    fmt_string = generator._ScriptGenerator__output_arch_to_ldscript()
    assert fmt_string == "OUTPUT_ARCH(i386)"


def test_entry_point_to_ldscript():
    generator = pyl.ScriptGenerator()
    generator.entry_point = "x64::initialize"
    fmt_string = generator._ScriptGenerator__entry_point_to_ldscript()
    assert fmt_string == 'ENTRY("x64::initialize")'


def test_construct_ldscript():
    """ construct_ldscript must create a valid ldscript"""
    generator = pyl.ScriptGenerator()
    generator.entry_point = "my_entry"
    generator.architecture = pyl.OutputArch.X86_64
    generator.object_format = pyl.OutputFormat.ELF64_X86_64

    generator.add_memory_region(
        "RAM",
        0x20000000,
        pyl.RegionLength(12, pyl.MemoryUnit.KILO),
        [pyl.RegionAttr.EXECUTABLE, pyl.RegionAttr.READWRITE],
    )
    generator.add_memory_region(
        "ROM",
        0x08000000,
        pyl.RegionLength(64, pyl.MemoryUnit.KILO),
        [pyl.RegionAttr.EXECUTABLE, pyl.RegionAttr.READONLY],
    )

    script = generator._ScriptGenerator__construct_ldscript()
    expected = """OUTPUT_FORMAT(elf64-x86-64)
OUTPUT_ARCH(i386:x86-64)
ENTRY(\"my_entry\")

MEMORY {
    RAM (xw): ORIGIN = 0x20000000, LENGTH = 12K
    ROM (xr): ORIGIN = 0x8000000, LENGTH = 64K
}
"""
    assert script == expected

    # error handling
    delattr(generator, "architecture")
    err = generator._ScriptGenerator__construct_ldscript()
    assert err == pyl.PyLinkageError(
        msg="Not found such an attribute => 'architecture'"
    )
