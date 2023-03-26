from typing import List
from dataclasses import dataclass


@dataclass
class BackboneDevice:
    id: int
    name: str
    type: str
    os_version: str
    bb_links: List[int]
    clients: List[int]
