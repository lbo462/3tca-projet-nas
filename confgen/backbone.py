import json
from typing import List

from .settings import APP_ARGS
from .exceptions import BadlyFormedJSON, AppError
from .backbone_device import BackboneDevice
from .client import Client
from .gns3 import GNS3Config, GNS3Device


class Backbone:
    _edge_routers: List[BackboneDevice]
    _core_routers: List[BackboneDevice]
    _clients: List[Client]

    _gns3_devices: List[GNS3Device]

    def __init__(self, config_file_path: str, gns3_config: GNS3Config):
        """

        :param config_file_path: Path to the JSON config file
        :param gns3_config: gns3 config
        :raises BadlyFormedJSON: When keys in the config file are not the one excepted
        """
        self._edge_routers = []
        self._core_routers = []
        self._clients = []

        self._gns3_devices = []

        # Load config file
        with open(config_file_path, "r") as f:
            config_dict_full = json.loads(f.read())

        # Verify keys
        if "backbone_devices" not in config_dict_full:
            raise BadlyFormedJSON(
                f'"backbone_device" key not found in {config_file_path}'
            )

        if "clients" not in config_dict_full:
            raise BadlyFormedJSON(f'"clients" key not found in {config_file_path}')

        # Create dicts
        config_dict_backbone_devices = config_dict_full["backbone_devices"]
        config_dict_clients = config_dict_full["clients"]

        # Create backbone devices
        for backbone_device_dict in config_dict_backbone_devices:
            backbone_device = BackboneDevice(backbone_device_dict)

            # Create gns3 device
            port = -1  # Search telnet port for this device
            for node in gns3_config.nodes:
                if node.name == backbone_device.name:
                    port = node.console
            if port == -1:
                raise AppError(f"`{backbone_device.name}` not found on GNS3.")
            self._gns3_devices.append(
                GNS3Device(backbone_device, gns3_config.host, port)
            )

            # Sort by type
            if backbone_device.type == "edge":
                self._edge_routers.append(backbone_device)
            elif backbone_device.type == "core":
                self._core_routers.append(backbone_device)
            else:
                raise AppError(
                    f"Router type `{backbone_device}` is invalid. Valid types are `edge` and `core`"
                )

        # Create clients
        for client_dict in config_dict_clients:
            self._clients.append(Client(client_dict))

        # Inform edge routers of backbone and clients infrastructure
        for edge_router in self._edge_routers:
            edge_router.set_edge(self._edge_routers, self._clients)

    def get_all_configs(self) -> str:
        """

        :return: Written list of every confs
        """
        confs = "--- Configurations of core routers ---\n"
        for core_router in self._core_routers:
            confs += core_router.get_config()

        confs += "--- Configurations of edge routers ---\n"
        for edge_router in self._edge_routers:
            confs += edge_router.get_config()

        return confs

    def write_configs(self) -> str:
        """
        Write configs on GNS3
        ! This process can be long because of routers CLI !
        :return: Every config written on each device
        """
        log = "--- GNS3 write recap ---\n"
        for gns3_device in self._gns3_devices:
            if APP_ARGS.verbose:
                print(f">> Configuring {gns3_device.name} ...")
            log += f"-- Configuration written to {gns3_device.name} --\n"
            log += gns3_device.write() + "\n"
        log += "--- end of GNS3 recap ---"
        return log
