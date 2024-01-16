from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    state_code: Mapped[str] = mapped_column(String(2))
    state_name: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    county: Mapped[str] = mapped_column(String(50))
    geo_location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )
