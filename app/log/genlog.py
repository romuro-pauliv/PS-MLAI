# |--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                  app/log/genlog.py |
# |                                                                                                    encoding: UTF-8 |
# |                                                                                                     Python v: 3.10 |
# |--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama   import Fore, Style
from datetime   import datetime
from typing     import Union

import inspect
# |--------------------------------------------------------------------------------------------------------------------|
import logging
from colorama import Fore, Style
from datetime import datetime
from typing import Union
import inspect

class StringLog:
    """
    A class to generate formatted log messages with optional color coding.
    """

    def __init__(self) -> None:
        self.color: bool = False

    def active_color(self) -> None:
        self.color = True

    def datetime_func(self) -> str:
        if self.color:
            return f"[{Fore.CYAN}{datetime.now()}{Style.RESET_ALL}]"
        return f"[{datetime.now()}]"

    def instance_func(self, value: str) -> str:
        if self.color:
            return f"[{Fore.MAGENTA}{value}{Style.RESET_ALL}]"
        return f"[{value}]"

    def method_func(self, value: str) -> str:
        if self.color:
            return f"({Fore.LIGHTMAGENTA_EX}{value}{Style.RESET_ALL})]"
        return f"({value})]"

    def success_func(self, value: Union[bool, str]) -> str:
        if self.color:
            if isinstance(value, bool):
                return f"[{Fore.GREEN if value else Fore.RED}{'SUCCESS' if value else 'FAILED'}{Style.RESET_ALL}]"
            return f"[{Fore.YELLOW}{value.upper()}{Style.RESET_ALL}]"

        if isinstance(value, bool):
            return f"[{'SUCCESS' if value else 'FAILED'}]"
        return f"[{value.upper()}]"

    def info_func(self, value: str) -> str:
        return value


class GenLog(StringLog):
    """
    A class to generate and print detailed log messages with verbosity control.
    """

    def __init__(self) -> None:
        self.verbose: bool = False
        super().__init__()

        # Configure logger
        self.logger = logging.getLogger("GenLog")
        handler = logging.StreamHandler()  # Logs to stdout
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)  # Default level
        self.logger.setLevel(logging.ERROR)

    def active_verbose(self) -> None:
        self.verbose = True
        self.logger.setLevel(logging.DEBUG)  # Enable verbose logs

    def log(self, status: bool, info: str, v: bool) -> None:
        frame = inspect.currentframe()
        outer_frame = inspect.getouterframes(frame)[1]
        method_name: str = outer_frame.function
        try:
            instance = outer_frame.frame.f_locals['self']
            class_name: str = instance.__class__.__name__
        except KeyError:
            class_name: str = "global"

        datetime_log: str = self.datetime_func()
        instance_log: str = self.instance_func(class_name)
        method_log: str = self.method_func(method_name)
        success_log: str = self.success_func(status)
        info_log: str = self.info_func(info)

        log_message: str = f"{instance_log} {method_log} {success_log} | {info_log}"
        
        if status is False:
            self.logger.error(log_message)
            return None
        
        if v and self.verbose:
            self.logger.debug(log_message)
        elif not v:
            if status is False:
                self.logger.error(log_message)
            else:
                self.logger.info(log_message)
            


