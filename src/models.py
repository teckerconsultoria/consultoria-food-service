from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Restaurante:
    place_id: str
    nome: str
    endereco: str
    bairro: str
    lat: float
    lng: float
    tipo: str
    rating: Optional[float]
    price_level: Optional[int]
    tem_website: bool
    permanently_closed: bool
    data_coleta: datetime

    def to_dict(self) -> dict:
        return {
            "place_id": self.place_id,
            "nome": self.nome,
            "endereco": self.endereco,
            "bairro": self.bairro,
            "lat": self.lat,
            "lng": self.lng,
            "tipo": self.tipo,
            "rating": self.rating,
            "price_level": self.price_level,
            "tem_website": self.tem_website,
            "permanently_closed": self.permanently_closed,
            "data_coleta": self.data_coleta.isoformat() if self.data_coleta else None,
        }
