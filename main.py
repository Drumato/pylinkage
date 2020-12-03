import pylinkage as pyl


def main():
    generator = pyl.Generator()
    generator.architecture = pyl.OutputArch.X86_64
    # generator.object_format = pyl.OutputFormat.ELF64_X86_64
    generator.mode = pyl.OutputMode.SCRIPT
    generator.entry_point = "_start"

    if (err := generator.output_script("sample.scr")) != None:
        print(err)
        exit(1)


if __name__ == "__main__":
    main()

