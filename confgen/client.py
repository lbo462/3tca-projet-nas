from dataclasses import dataclass
from typing import Dict, List

from .client_ce import ClientCE
from .exceptions import BadlyFormedJSON


@dataclass
class Client:
    id: int
    name: str
    ce: List[ClientCE]

    def __init__(self, client_dict: Dict):
        self.ce = []

        try:
            self.id = client_dict["id"]
            self.name = client_dict["name"]
            for client_ce_dict in client_dict["ce"]:
                self.ce.append(ClientCE(self.id, client_ce_dict))
        except KeyError as e:
            raise BadlyFormedJSON(f"Client badly formed in JSON : {e}")
