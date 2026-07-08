from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


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
    telefone: Optional[str] = None
    horarios: Optional[dict] = None
    dining_options: Optional[dict] = None
    serves: Optional[dict] = None
    atmosphere: Optional[dict] = None
    payment_options: Optional[dict] = None
    parking: Optional[dict] = None
    accessibility: Optional[dict] = None
    review_summary: Optional[str] = None
    photo_count: Optional[int] = None
    editorial_summary: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
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
            "telefone": self.telefone,
            "horarios": self.horarios,
            "dining_options": self.dining_options,
            "serves": self.serves,
            "atmosphere": self.atmosphere,
            "payment_options": self.payment_options,
            "parking": self.parking,
            "accessibility": self.accessibility,
            "review_summary": self.review_summary,
            "photo_count": self.photo_count,
            "editorial_summary": self.editorial_summary,
        }
