from dataclasses import dataclass
from typing import List, Dict


class AppError(Exception):
    pass


class NeighborNotLinked(Exception):
    pass


@dataclass
class BackboneDevice:
    id: int
    name: str
    type: str
    os_version: str
    bb_links: List[int]
    # clients: List[str] # required if type == "edge"

    def __init__(self, device_dict: Dict):
        try:
            self.id = device_dict["id"]
            self.name = device_dict["name"]
            self.type = device_dict["type"]
            self.os_version = device_dict["os_version"]
            self.bb_links = device_dict["bb_links"]

            if self.type == "edge":
                self.clients = device_dict["clients"]
        except KeyError:
            raise AppError("Badly formed dict")

    def get_ip(self, neighbor_id: int) -> str:
        """
        Returns the ip address linked to a neighbor
        :raises NeighborNotLinked: if neighbor_id is not in bb_links
        """

        if neighbor_id not in self.bb_links:
            raise NeighborNotLinked(
                f"Neighbor #{neighbor_id} is not in bb_links for router {self.id}"
            )

        # finds out biggest and lowest ID
        bid = max(self.id, neighbor_id)
        lid = min(self.id, neighbor_id)

        # choose on which side of the link is self
        side = 1 if self.id == bid else 2

        # compute the IP@ to be unique in the network
        first_byte = int(bid / 255)
        second_byte = bid % 255
        third_byte = lid % 255
        fourth_byte = (int(lid / 255) << 2) + side

        return f"{first_byte}.{second_byte}.{third_byte}.{fourth_byte}"
