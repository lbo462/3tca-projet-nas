from telnetlib import Telnet
from time import sleep

from backbone_device import BackboneDevice


CLI_DELAY = 0.5


class GNS3Device:
    def __init__(self, bb_device: BackboneDevice, host: str, port: int):
        self._bb_device = bb_device
        self._host = host
        self._port = port

    def write(self):
        """
        Write config to GNS3 router
        """
        with Telnet(self._host, self._port) as tn:

            def write(line_: str):
                """
                Transform line to byte and send to router with a delay
                """
                tn.write(bytearray(f"{line_}\r", "utf-8"))
                sleep(CLI_DELAY)

            # Retrieve config
            config = self._bb_device.get_config()

            # Enable router CLI
            write("en")

            # Enable router CLI
            write("conf t")

            for line in config.split("\n"):
                if not line.startswith("!"):
                    write(line)

            # Exit config mode
            write("end")

            # Write changes to startup config
            write("write")
