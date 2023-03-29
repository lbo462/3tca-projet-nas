import json
import gns3fy

from exceptions import AppError
from backbone_device import BackboneDevice
from gns3_device import GNS3Device

JSON_FILE_NAME = "bb_config.json"

HOST = "localhost"
PORT = 3080
PROJECT_NAME = "ProjetNAS"


def main():
    # Connect to GNS3 server
    gns3_server = gns3fy.Gns3Connector(f"http://{HOST}:{PORT}")

    # Retrieve project
    lab = gns3fy.Project(name=PROJECT_NAME, connector=gns3_server)
    lab.get()

    # Open project
    lab.open()

    # Retrieve raw high level configuration
    with open(JSON_FILE_NAME, "r") as f:
        raw_file = f.read()
    conf_dict = json.loads(raw_file)

    if "backbone_devices" not in conf_dict:
        raise AppError("backbone_devices not in JSON.")

    # Loop though devices
    for backbone_device_dict in conf_dict["backbone_devices"]:
        # Create backbone device
        backbone_device = BackboneDevice(backbone_device_dict)

        # Find telnet port for GNS3Device
        # not very clean but does the job
        port = -1
        for node in lab.nodes:
            if node.name == backbone_device.name:
                port = node.console
        if port == -1:
            raise AppError(f"{backbone_device.name} not found on GNS3 project.")

        # Create gns3_device object from its dict
        gns3_device = GNS3Device(backbone_device, HOST, port)

        print(f"Created {backbone_device.name} :\n\n{backbone_device.get_config()}")

        # Write conf on routers
        # gns3_device.write()
        print(f"Configuration for {backbone_device.name} written on GNS3 !\n")


if __name__ == "__main__":
    main()
