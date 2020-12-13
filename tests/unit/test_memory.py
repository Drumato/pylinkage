import pylinkage as pyl


def test_memory_region_to_ldscript():
    region = pyl.Region(
        "ABC", None, 0x20000000, pyl.RegionLength(12, pyl.MemoryUnit.KILO)
    )
    assert region.to_ldscript() == "ABC : ORIGIN = 0x20000000, LENGTH = 12K"