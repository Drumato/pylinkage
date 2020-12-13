# pylinkage

Linker Script in Python

## test

```shell
$ python task_runner.py test
```

## How to Run

### Build

```
git clone git@github.com:Drumato/pylinkage.git && cd pylinkage
pip install ./
```

### Sample

See [main.py](./main.py).  

```python
import pylinkage as pyl


def main():
    generator = pyl.ScriptGenerator()
    generator.architecture = pyl.OutputArch.X86_64
    generator.object_format = pyl.OutputFormat.ELF64_X86_64
    generator.entry_point = "_start"

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

    if (err := generator.output_ldscript("sample.scr")) != None:
        print(err)
        exit(1)


if __name__ == "__main__":
    main()

```
