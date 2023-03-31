from typing import List, Dict

from exceptions import NeighborNotLinked, AppError
from constants import ASN, OSPF_PROCESS, OSPF_AREA, INTERCO_MASK
from client import Client
from client_ce import ClientCE


# NETWORK SETUP
INTERFACE_NAMES = [
    "GigabitEthernet1/0",
    "GigabitEthernet2/0",
    "GigabitEthernet3/0",
]


class BackboneDevice:
    def __init__(self, device_dict: Dict):
        """

        :param device_dict: Dict from JSON config file
        """

        # Define empty list for future config
        self._edge_routers = []
        self._clients_ce: List[ClientCE] = []

        try:
            self.id = device_dict["id"]
            self._name = device_dict["name"]
            self.type = device_dict["type"]
            self._os_version = device_dict["os_version"]  # Useless but RP
            self._bb_links = device_dict["bb_links"]

            if self.type == "edge":
                self._clients_id = device_dict["clients"]
        except KeyError:
            raise AppError("Badly formed dict.")

        self._interfaces = INTERFACE_NAMES

        if len(self._bb_links) > len(self._interfaces):
            raise AppError(
                f"Too much links for {self._name} links. Only {len(self._interfaces)} interfaces are connected."
            )

    def set_edge(self, edge_routers: List, every_clients: List[Client]):
        """
        Retrieve necessary information
        :param edge_routers: edges routers of the backbone. Only necessary for edge routers
        :param every_clients: a list of every client. Only necessary for edge routers
        """
        if self.type != "edge":
            raise AppError(
                f"`set_edge` should only be called on edge routers. {self.type} is invalid"
            )

        self._edge_routers = edge_routers

        # Collect connected ce clients from the list of every client
        for client in every_clients:
            for ce in client.ce:
                if [client.id, ce.id] in self._clients_id:
                    self._clients_ce.append(ce)

    @property
    def name(self):
        return self._name

    @property
    def formatted_id(self):
        return f"{self.id}.{self.id}.{self.id}.{self.id}"

    @property
    def bgp_id(self):
        return f"1.0.0.{self.id}"

    def get_config(self) -> str:
        """
        Return the config to write on the router
        """
        conf = f"""! Global config for {self.name} #({self.id})       
!
"""

        # ------------
        # Global config
        # ------------

        # OSPF
        conf += f"""! Global OSPF config
router ospf {OSPF_PROCESS}
router-id {self.formatted_id}
ip ospf network point-to-point
mpls ldp autoconfig area {OSPF_AREA}
exit
"""
        # BGP
        if self.type == "edge":
            conf += "! BGP/ VPN config\n"

            for ce in self._clients_ce:
                conf += f"""! VRF
vrf destination {ce.formatted_name}
address-family ipv4
rd {100 + ce.client_id}:{ce.id}
route-target both 1000:{1000 + ce.id}
"""
                for vpn_connection in ce.vpn_connections:
                    conf += f"route-target import 1000:{1000 + vpn_connection}\n"

            conf += f"""! ---
router bgp {ASN}
bgp router-id {self.bgp_id}
"""

            # Configure connection to every other edge routers
            for edge_router in self._edge_routers:
                if self.id == edge_router.id:  # Ignore self
                    continue

                pe_id = edge_router.formatted_id
                conf += f"""! BGP config for {edge_router.name} #({edge_router.id})
neighbor {pe_id} remote-as {ASN}
address-family vpnv4
neighbor {pe_id} activate
neighbor {pe_id} update-source Loopback0
neighbor {pe_id} next-hop-self
exit
"""

            conf += "exit\n"  # exit BGP configuration

        # MPLS
        conf += f"""! MPLS config
int loopback 0
ip address {self.formatted_id} 255.255.255.255
ip ospf {OSPF_PROCESS} area {OSPF_AREA}
exit    
"""

        # ------------
        # Neighbor based config
        # ------------

        interface_counter = 0

        # Intra-backbone links
        for n_id in self._bb_links:
            ip_addr_on_int = self._get_ip(n_id)  # IP@ on interface facing neighbor

            conf += f"""!
! Configuration for neighbor {n_id} on {self._interfaces[interface_counter]}
!
"""

            # interface
            conf += f"""interface {self._interfaces[interface_counter]}
ip address {ip_addr_on_int} {INTERCO_MASK}
no shut
exit
"""
            # OSPF
            conf += f"""router ospf {OSPF_PROCESS}
network {ip_addr_on_int} 0.0.0.0 area {OSPF_AREA}
exit
"""

            # MPLS
            conf += f"""mpls ldp router-id Loopback 0 force
interface {self._interfaces[interface_counter]}
mpls ip
exit
"""
            interface_counter += 1

        # Links to clients
        for ce in self._clients_ce:

            # interface
            conf += f"""interface {self._interfaces[interface_counter]}
ip address {ce.ip_addr}
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
                f"Neighbor #{neighbor_id} is not in bb_links for router {self.id}"
            )

        # finds out biggest and lowest ID
        bid = max(self.id, neighbor_id)
        lid = min(self.id, neighbor_id)

        # choose on which side of the link is self
        side = 1 if self.id == bid else 2

        # compute the IP@ to be unique in the network
        first_byte = int(bid / 255) + 1
        second_byte = bid % 255
        third_byte = lid % 255
        fourth_byte = (int(lid / 255) << 2) + side

        return f"{first_byte}.{second_byte}.{third_byte}.{fourth_byte}"
