import json

from backbone_device import BackboneDevice


def main():
    with open("bb_config.json", "r") as f:
        raw_file = f.read()
    conf_dict = json.loads(raw_file)

    for backbone_device_dict in conf_dict["backbone_devices"]:
        # create backbone_device object from its dict
        backbone_device = BackboneDevice(backbone_device_dict)

        print(f"Created {backbone_device.name} :\n{backbone_device.get_config()} \n")


if __name__ == "__main__":
    main()
