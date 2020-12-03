import pylinkage as pyl


def test_output_format_to_ldscript():
    generator = pyl.Generator()
    generator.object_format = pyl.OutputFormat.ELF64_X86_64
    fmt_string = generator.output_format_to_ldscript()
    assert fmt_string == "OUTPUT_FORMAT(elf64-x86-64)"

    # check how its failure
    delattr(generator, "object_format")
    fmt_string = generator.output_format_to_ldscript()
    assert fmt_string == pyl.PyLinkageError(
        msg="Not found such an attribute => 'object_format'"
    )


def test_output_arch_to_ldscript():
    generator = pyl.Generator()
    generator.architecture = pyl.OutputArch.I386
    fmt_string = generator.output_arch_to_ldscript()
    assert fmt_string == "OUTPUT_ARCH(i386)"


def test_entry_point_to_ldscript():
    generator = pyl.Generator()
    generator.entry_point = "x64::initialize"
    fmt_string = generator.entry_point_to_ldscript()
    assert fmt_string == 'ENTRY("x64::initialize")'


def test_construct_ldscript():
    """ construct_ldscript must create a valid ldscript"""
    generator = pyl.Generator()
    generator.entry_point = "my_entry"
    generator.architecture = pyl.OutputArch.X86_64
    generator.object_format = pyl.OutputFormat.ELF64_X86_64

    script = generator.construct_ldscript()
    expected = """OUTPUT_FORMAT(elf64-x86-64)
OUTPUT_ARCH(x86-64)
ENTRY(\"my_entry\")
"""
    assert script == expected

    # error handling
    delattr(generator, "architecture")
    err = generator.construct_ldscript()
    assert err == pyl.PyLinkageError(
        msg="Not found such an attribute => 'architecture'"
    )
