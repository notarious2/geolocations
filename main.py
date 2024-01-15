import csv

from fastapi import Depends, FastAPI
from geoalchemy2.functions import ST_DWithin, ST_GeogFromText, ST_GeogFromWKB
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import City
from schemas import CitySchema, NearbyCitiesByCoordsSchema, NearbyCitiesSchema
from services import is_city_table_empty

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/load-cities")
async def load_cities(db_session: AsyncSession = Depends(get_async_session)):
    if await is_city_table_empty(db_session):
        cities = []
        with open("us_cities.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")

            # Skip the first row (header)
            next(csv_reader)

            for row in csv_reader:
                city = City(
                    state_code=row[1],
                    state_name=row[2],
                    city=row[3],
                    county=row[4],
                    geo_location=f"POINT({row[5]} {row[6]})",
                )
                cities.append(city)

            db_session.add_all(cities)
            await db_session.commit()
            return {"message": "Data loaded successfully"}

    return {"message": "Data is already loaded"}


@app.get("/cities", response_model=list[CitySchema])
async def get_cities(db_session: AsyncSession = Depends(get_async_session)):
    result = await db_session.execute(select(City))
    cities = result.scalars().all()[:100]
    return cities


@app.post("/nearby-cities-by-details")
async def get_nearby_cities_by_details(
    nearby_cities_schema: NearbyCitiesSchema,
    db_session: AsyncSession = Depends(get_async_session),
):
    city, county, state_code, km_within = (
        nearby_cities_schema.city,
        nearby_cities_schema.county,
        nearby_cities_schema.state_code,
        nearby_cities_schema.km_within,
    )

    # Check if the target city exists and retrieve its geography
    target_city_query = select(City).where(
        and_(City.city == city, City.state_code == state_code, City.county == county)
    )
    result = await db_session.execute(target_city_query)
    target_city = result.scalar_one_or_none()

    # If the target city is not found, return an error message
    if not target_city:
        return {"message": "City was not found"}

    # Extract the geography of the target city
    target_geography = ST_GeogFromWKB(target_city.geo_location)

    # Query nearby cities within the specified distance from the target city
    nearby_cities_query = select(City.city).where(
        ST_DWithin(City.geo_location, target_geography, 1000 * km_within)
    )
    result = await db_session.execute(nearby_cities_query)
    nearby_cities = result.scalars().all()

    return nearby_cities


@app.post("/nearby-cities-by-coordinates")
async def get_nearby_cities_by_coords(
    coords_schema: NearbyCitiesByCoordsSchema,
    db_session: AsyncSession = Depends(get_async_session),
):
    lat, long, km_within = (
        coords_schema.lat,
        coords_schema.long,
        coords_schema.km_within,
    )

    target_geography = ST_GeogFromText(f"POINT({lat} {long})", srid=4326)

    nearby_cities_query = select(City.city).where(
        ST_DWithin(City.geo_location, target_geography, 1000 * km_within)
    )
    result = await db_session.execute(nearby_cities_query)
    nearby_cities = result.scalars().all()

    return nearby_cities
