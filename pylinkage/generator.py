from dataclasses import dataclass, field
from .output_mode import OutputMode
from .output_format import OutputFormat
from .output_arch import OutputArch
from .error import PyLinkageError

from typing import Optional, Union


@dataclass
class Generator:
    """Linker Configuration Generator.

    Attributes:
        mode (OutputMode): Select the format that generator output configuration as.
        object_format (OutputFormat): Specify the output format of executable.
        architecture (OutputArch): Specify a particular output machine architecture.
        entry_point (str): Define the first executable instruction in an output file
    """

    mode: OutputMode = field(default=OutputMode.SCRIPT, init=False)
    object_format: OutputFormat = field(init=False)
    architecture: OutputArch = field(init=False)
    entry_point: str = field(default="_start", init=False)

    def output_format_to_ldscript(
        self,
    ) -> Union[str, PyLinkageError]:
        """
        translate OutputFormat to string like ldscript
        """
        print(self.check_certain_attribute_is_exist("object_format"))
        if (err := self.check_certain_attribute_is_exist("object_format")) != None:
            return err

        return f"OUTPUT_FORMAT({self.object_format.to_string()})"

    def output_arch_to_ldscript(self) -> Union[str, PyLinkageError]:
        """
        translate OutputArch to string like ldscript
        """
        if (err := self.check_certain_attribute_is_exist("architecture")) != None:
            return err
        return f"OUTPUT_ARCH({self.architecture.to_string()})"

    def entry_point_to_ldscript(self) -> Union[str, PyLinkageError]:
        """
        format entry_point like ldscript
        """
        if (err := self.check_certain_attribute_is_exist("entry_point")) != None:
            return err
        return f'ENTRY("{self.entry_point}")'

    def construct_ldscript(self) -> Union[str, PyLinkageError]:
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

        if (err := attribute_to_ldscript(self.output_format_to_ldscript)) != None:
            return err
        if (err := attribute_to_ldscript(self.output_arch_to_ldscript)) != None:
            return err
        if (err := attribute_to_ldscript(self.entry_point_to_ldscript)) != None:
            return err

        return script

    def construct_script(self) -> Union[str, PyLinkageError]:
        """
        construct a script by output mode
        """
        if (err := self.check_certain_attribute_is_exist("mode")) != None:
            return err

        if self.mode == OutputMode.YAML:
            return "UNIMPLEMENTED!"
        else:
            return self.construct_ldscript()

    def output_script(self, file_name: str) -> Optional[PyLinkageError]:
        with open(file_name, "w") as f:
            if isinstance((result := self.construct_script()), PyLinkageError):
                return result
            else:
                f.write(result)

        return None

    def check_certain_attribute_is_exist(
        self,
        attribute_name: str,
    ) -> Optional[PyLinkageError]:
        if not hasattr(self, attribute_name):
            return PyLinkageError().not_found_such_an_attribute(attribute_name)
        return None