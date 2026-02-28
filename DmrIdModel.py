from dataclasses import dataclass

@dataclass
class DmrIdModel:
    id: int
    callsign: str
    city: str
    country: str
    fname: str
    state: str
    surname: str
    
