from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from geoalchemy2 import Geometry, WKBElement
from database import Base


class City(Base):
    __tablename__ = "city"

    id = mapped_column(Integer, primary_key=True)
    state_code = mapped_column(String(2))
    state_name = mapped_column(String(50))
    city = mapped_column(String(50))
    county = mapped_column(String(50))
    geo_location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )
