from dataclasses import dataclass
from typing import List, Dict


class AppError(Exception):
    pass


class NeighborNotLinked(Exception):
    pass


# NETWORK SETUP
INTERFACE_NAMES = [
    "GigabitEthernet1/0",
    "GigabitEthernet2/0",
    "GigabitEthernet3/0",
]
INTERCO_MASK = "255.255.255.242"

# OSPF CONFIG
OSPF_AREA = "0"
OSPF_PROCESS = "10"


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
    
    @property
    def _ospf_id(self):
        return f"{self._id}.{self._id}.{self._id}.{self._id}"
        
    def get_config(self) -> str:
        """
        Return the config to write on the router
        """
        conf = "conf t"  # conf is sent as CLI

        # ------------
        # Global config
        # ------------

        conf += f"""
router ospf 10
router-id {self._ospf_id}
exit
"""

        # ------------
        # Neighbor based config
        # ------------
        for i, n_id in enumerate(self._bb_links):

            ip_addr_on_int = self._get_ip(n_id)  # IP@ on interface facing neighbor

        # configure interface
            conf += f"""interface {self._interfaces[i]}
ip address {ip_addr_on_int} {INTERCO_MASK}
no shut
exit
"""
        # configure OSPF
            conf += f"""router ospf {OSPF_PROCESS}
network {ip_addr_on_int} 0.0.0.0 area {OSPF_AREA}
exit
"""

        # conf += "write"

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
