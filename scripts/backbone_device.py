from typing import List, Dict

from exceptions import NeighborNotLinked, AppError


# NETWORK SETUP
INTERFACE_NAMES = [
    "GigabitEthernet1/0",
    "GigabitEthernet2/0",
    "GigabitEthernet3/0",
]
INTERCO_MASK = "255.255.255.252"

# OSPF CONFIG
OSPF_AREA = 0
OSPF_PROCESS = 10

# BGP CONFIG
ASN = 100


class BackboneDevice:
    _id: int
    _name: str
    type: str
    _os_version: str
    _bb_links: List[int]
    # clients: List[str] # required if type == "edge"
    _interfaces: List[str]

    def __init__(self, device_dict: Dict):
        try:
            self._id = device_dict["id"]
            self._name = device_dict["name"]
            self.type = device_dict["type"]
            self._os_version = device_dict["os_version"]
            self._bb_links = device_dict["bb_links"]

            if self.type == "edge":
                self._clients = device_dict["clients"]
        except KeyError:
            raise AppError("Badly formed dict.")

        self._interfaces = INTERFACE_NAMES

        if len(self._bb_links) > len(self._interfaces):
            raise AppError(
                f"Too much links for {self._name} links. Only {len(self._interfaces)} interfaces are connected."
            )

    @property
    def name(self):
        return self._name

    @property
    def _formatted_id(self):
        return f"{self._id}.{self._id}.{self._id}.{self._id}"

    @property
    def _bgp_id(self):
        return f"1.0.0.{self._id}"

    def get_config(self) -> str:
        """
        Return the config to write on the router
        """
        conf = f"""! Global config for {self.name} #({self._id})       
!
"""

        # ------------
        # Global config
        # ------------

        # OSPF
        conf += f"""router ospf {OSPF_PROCESS}
router-id {self._formatted_id}
ip ospf network point-to-point
mpls ldp autoconfig area {OSPF_AREA}
exit
"""
        # BGP
        if self.type == "edge":
            # configure BGP
            conf += f"""router bgp {ASN}
bgp router-id {self._bgp_id}
exit
"""

        # MPLS
        conf += f"""int loopback 0
ip address {self._formatted_id} 255.255.255.255
ip ospf {OSPF_PROCESS} area {OSPF_AREA}
exit    
"""

        # ------------
        # Neighbor based config
        # ------------
        for i, n_id in enumerate(self._bb_links):
            ip_addr_on_int = self._get_ip(n_id)  # IP@ on interface facing neighbor

            conf += f"""!
! Configuration for neighbor {n_id} on {self._interfaces[i]}
!
"""

            # interface
            conf += f"""interface {self._interfaces[i]}
ip address {ip_addr_on_int} {INTERCO_MASK}
no shut
exit
"""
            # OSPF
            conf += f"""router ospf {OSPF_PROCESS}
network {ip_addr_on_int} 0.0.0.0 area {OSPF_AREA}
exit
"""

            # BGP
            # TODO

            # MPLS
            conf += f"""mpls ldp router-id Loopback 0 force
interface {self._interfaces[i]}
mpls ip
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
        first_byte = int(bid / 255) + 1
        second_byte = bid % 255
        third_byte = lid % 255
        fourth_byte = (int(lid / 255) << 2) + side

        return f"{first_byte}.{second_byte}.{third_byte}.{fourth_byte}"
