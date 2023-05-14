from telnetlib import Telnet
from time import sleep
from typing import List
from dataclasses import dataclass

from .settings import APP_ARGS
from .backbone_device import BackboneDevice


CLI_DELAY = 0.5


@dataclass
class GNS3Config:
    host: str  # GNS3 server address
    nodes: List  # List of nodes extracted by gns3fy


class GNS3Device:
    def __init__(self, bb_device: BackboneDevice, host: str, port: int):
        self._bb_device = bb_device
        self._host = host
        self._port = port

        self.name = self._bb_device.name

    def write(self) -> str:
        """
        Write config to GNS3 router
        :return: Config written to the router
        """
        log = ""
        with Telnet(self._host, self._port) as tn:

            def write(line_: str) -> str:
                """
                Transform line to byte and send to router with a delay
                :return: passed arg (with a line break !)
                """
                if APP_ARGS.verbose:
                    print(
                        f"{'(dry) ' if APP_ARGS.dry_run else ''}{self.name} : {line_}"
                    )
                if not APP_ARGS.dry_run:
                    tn.write(bytearray(f"{line_}\r", "utf-8"))
                    sleep(CLI_DELAY)
                return line_ + "\n"

            # Retrieve config to write
            config = self._bb_device.get_config()

            # Enable router CLI
            log += write("en")

            # Enter config mode
            log += write("conf t")

            # Write every line of conf (ignoring comments)
            for line in config.split("\n"):
                if not line.startswith("!"):
                    log += write(line)

            # Exit config mode
            log += write("end")

            # Write changes to startup config
            log += write("write\r")

        return log
