from geoalchemy2.shape import to_shape
from pydantic import BaseModel, PositiveInt, field_validator
from pydantic_extra_types.coordinate import Latitude, Longitude


class CitySchema(BaseModel):
    state_code: str
    state_name: str
    city: str
    county: str
    geo_location: str

    @field_validator("geo_location", mode="before")
    def turn_geo_location_into_wkt(cls, value):
        return to_shape(value).wkt


class NearbyCitiesSchema(BaseModel):
    city: str
    county: str
    state_code: str
    km_within: PositiveInt


class NearbyCitiesByCoordsSchema(BaseModel):
    lat: Latitude
    long: Longitude
    km_within: PositiveInt
