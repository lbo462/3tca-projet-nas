from telnetlib import Telnet
from time import sleep

from backbone_device import BackboneDevice


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
            config = self._bb_device.get_config()

            for line in config.split("\n"):
                # Format line to bytes with \r
                line_as_byte = bytearray(f"{line}\r", "utf-8")

                # Write line to router
                tn.write(line_as_byte)

                # Keep router CLI alive
                sleep(0.5)

            tn.write(b"end\r")
            sleep(1)

