from dataclasses import dataclass, field
from typing import Optional, Union

from ..output_format import OutputFormat
from ..output_arch import OutputArch
from ..error import PyLinkageError
from ..memory import Region, RegionAttr, RegionLength


@dataclass
class ScriptGenerator:
    """Linker Script Generator.

    Attributes:
        object_format (OutputFormat): Specify the output format of executable.
        architecture (OutputArch): Specify a particular output machine architecture.
        entry_point (str): Define the first executable instruction in an output file.
        memory_regions (list[Region]): all available memory.
    """

    object_format: OutputFormat = field(init=False)
    architecture: OutputArch = field(init=False)
    entry_point: str = field(default="_start", init=False)
    memory_regions: list[Region] = field(default_factory=lambda: [], init=False)

    def output_ldscript(self, file_name: str) -> Optional[PyLinkageError]:
        """output an linker script"""
        with open(file_name, "w") as f:
            if isinstance((result := self.__construct_ldscript()), PyLinkageError):
                return result
            else:
                f.write(result)

        return None

    def add_memory_region(
        self,
        region_name: str,
        origin: int,
        length: RegionLength,
        attr: Optional[list[RegionAttr]] = None,
    ):
        """add a new memory-region"""
        region = Region(region_name, attr, origin, length)
        self.memory_regions.append(region)

    def __output_format_to_ldscript(
        self,
    ) -> Union[str, PyLinkageError]:
        """
        translate OutputFormat to string like ldscript
        """
        if (err := self.__check_certain_attribute_is_exist("object_format")) != None:
            return err

        return f"OUTPUT_FORMAT({self.object_format.to_string()})"

    def __output_arch_to_ldscript(self) -> Union[str, PyLinkageError]:
        """
        translate OutputArch to string like ldscript
        """
        if (err := self.__check_certain_attribute_is_exist("architecture")) != None:
            return err
        return f"OUTPUT_ARCH({self.architecture.to_string()})"

    def __entry_point_to_ldscript(self) -> Union[str, PyLinkageError]:
        """
        format entry_point like ldscript
        """
        if (err := self.__check_certain_attribute_is_exist("entry_point")) != None:
            return err
        return f'ENTRY("{self.entry_point}")'

    def __construct_ldscript(self) -> Union[str, PyLinkageError]:
        """
        construct linker script by Generator's attribute
        """
        script = ""

        # 毎回やるのは大変なのでクロージャで簡潔に
        def attribute_to_ldscript(f) -> Optional[PyLinkageError]:
            nonlocal script
            if isinstance((result := f()), PyLinkageError):
                return result
            else:
                script += result + "\n"
            return None

        if (err := attribute_to_ldscript(self.__output_format_to_ldscript)) != None:
            return err
        if (err := attribute_to_ldscript(self.__output_arch_to_ldscript)) != None:
            return err
        if (err := attribute_to_ldscript(self.__entry_point_to_ldscript)) != None:
            return err

        if len(self.memory_regions):
            script += "\n"
            script += "MEMORY {\n"
            for region in self.memory_regions:
                script += f"    {region.to_ldscript()}\n"
            script += "}\n"

        return script

    def __check_certain_attribute_is_exist(
        self,
        attribute_name: str,
    ) -> Optional[PyLinkageError]:
        if not hasattr(self, attribute_name):
            return PyLinkageError().not_found_such_an_attribute(attribute_name)
        return None