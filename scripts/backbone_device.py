from dataclasses import dataclass
from typing import List, Dict


class AppError(Exception):
    pass


class NeighborNotLinked(Exception):
    pass


INTERFACE_NAMES = [
    "GigabitEthernet0/0",
    "GigabitEthernet0/1",
    "GigabitEthernet0/2",
]

INTERCO_MASK = "255.255.255.242"


@dataclass
class BackboneDevice:
    _id: int
    _name: str
    _type: str
    _os_version: str
    _bb_links: List[int]
    # clients: List[str] # required if type == "edge"
    _interfaces: List[str]

    def __init__(self, device_dict: Dict):
        try:
            self._id = device_dict["id"]
            self._name = device_dict["name"]
            self._type = device_dict["type"]
            self._os_version = device_dict["os_version"]
            self._bb_links = device_dict["bb_links"]

            if self._type == "edge":
                self._clients = device_dict["clients"]
        except KeyError:
            raise AppError("Badly formed dict")
        
        self._interfaces = INTERFACE_NAMES
        
    @property
    def name(self):
        return self._name
        
    def get_config(self) -> str:
        """
        Return the config to write on the router
        """
        conf = "conf t"  # conf is sent as CLI

        # ------------
        # Global config
        # ------------


        # ------------
        # Neighbor based config
        # ------------
        for i, n_id in enumerate(self._bb_links):
            conf += f"""
interface {self._interfaces[i]}
ip address {self._get_ip(n_id)} {INTERCO_MASK}
no shut
exit
"""

        return conf

    def _get_ip(self, neighbor_id: int) -> str:
        """
        Returns the ip address linked to a neighbor
        :raises NeighborNotLinked: if neighbor_id is not in bb_links
        """

        if neighbor_id not in self._bb_links:
            raise NeighborNotLinked(
                f"Neighbor #{neighbor_id} is not in bb_links for router {self._id}"
            )

        # finds out biggest and lowest ID
        bid = max(self._id, neighbor_id)
        lid = min(self._id, neighbor_id)

        # choose on which side of the link is self
        side = 1 if self._id == bid else 2

        # compute the IP@ to be unique in the network
        first_byte = int(bid / 255)
        second_byte = bid % 255
        third_byte = lid % 255
        fourth_byte = (int(lid / 255) << 2) + side

        return f"{first_byte}.{second_byte}.{third_byte}.{fourth_byte}"
