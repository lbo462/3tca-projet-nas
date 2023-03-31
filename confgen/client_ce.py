from dataclasses import dataclass
from typing import List, Dict

from .exceptions import BadlyFormedJSON


@dataclass
class ClientCE:
    id: int
    client_id: int
    name: str
    ip_addr: str
    vpn_connections: List[int]

    def __init__(self, client_id: int, client_ce_dict: Dict):
        self.client_id = client_id
        try:
            self.id = client_ce_dict["id"]
            self.name = client_ce_dict["name"]
            self.ip_addr = client_ce_dict["ip_addr"]
            self.vpn_connections = client_ce_dict["vpn_connections"]
        except KeyError:
            raise BadlyFormedJSON("Client CE from JSON is badly formed.")

    @property
    def formatted_name(self):
        return self.name.replace(" ", "_")
