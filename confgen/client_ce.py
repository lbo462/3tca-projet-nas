from dataclasses import dataclass
from typing import List, Dict

from .exceptions import BadlyFormedJSON


@dataclass
class ClientCE:
    id: int
    client_id: int
    asn: int
    name: str
    ip_addr_client_side: str
    ip_addr_bb_side: str
    vpn_connections: List[int]

    def __init__(self, client_id: int, client_ce_dict: Dict):
        self.client_id = client_id
        try:
            self.id = client_ce_dict["id"]
            self.asn = client_ce_dict["asn"]
            self.name = client_ce_dict["name"]
            self.ip_addr_client_side = client_ce_dict["ip_addr_client_side"]
            self.ip_addr_bb_side = client_ce_dict["ip_addr_bb_side"]
            self.vpn_connections = client_ce_dict["vpn_connections"]
        except KeyError as e:
            raise BadlyFormedJSON(f"Client CE from JSON is badly formed. : {e}")

    @property
    def formatted_name(self):
        return self.name.replace(" ", "_")
