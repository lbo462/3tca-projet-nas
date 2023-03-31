import json
from typing import List

import exceptions
from backbone_device import BackboneDevice
from client import Client


class Backbone:
    _edge_routers: List[BackboneDevice]
    _core_routers: List[BackboneDevice]
    _clients: List[Client]

    def __init__(self, config_file_path: str):
        """

        :param config_file_path: Path to the JSON config file
        :raises BadlyFormedJSON: When keys in the config file are not the one excepted
        """

        # Load config file
        with open(config_file_path, "r") as f:
            config_dict_full = json.loads(f.read())

        # Verify keys
        if "backbone_devices" not in config_dict_full:
            raise exceptions.BadlyFormedJSON(
                f'"backbone_device" key not found in {config_file_path}'
            )

        if "clients" not in config_dict_full:
            raise exceptions.BadlyFormedJSON(
                f'"clients" key not found in {config_file_path}'
            )

        # Create dicts
        config_dict_backbone_devices = config_dict_full["backbone_devices"]
        config_dict_clients = config_dict_full["clients"]

        # Create backbone devices
        for backbone_device_dict in config_dict_backbone_devices:
            backbone_device = BackboneDevice(backbone_device_dict)

            # Sort by type
            if backbone_device.type == "edge":
                self._edge_routers.append(backbone_device)
            elif backbone_device.type == "core":
                self._core_routers.append(backbone_device)
            else:
                raise exceptions.AppError(
                    f"Router type `{backbone_device}` is invalid. Valid types are `edge` and `core`"
                )

        # Create clients
        for client_dict in config_dict_clients:
            self._clients.append(Client(client_dict))

    def config(self):
        pass
