import openai

from app.accessdata.datatypes import Base, Provider
from app.accessdata.geolocation import get_gps_coordinates

from geoalchemy2.elements import WKTElement
from sqlalchemy import create_engine, Engine, func
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker


DB_USER = "postgres"
DB_PASSWORD = "buruk101"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "outfoxhealth"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def setup_database() -> Engine:
    """Set up the database connection and create tables if they do not exist."""

    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as connection:
            print("Successfully connected to PostgreSQL!")
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
    
    Base.metadata.create_all(engine)
    
    return engine


engine = setup_database()

def get_engine() -> Engine:
    return engine


def object_as_dict(obj):
    """Converts a SQLAlchemy ORM object to a dictionary."""
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs if c.key != 'location'}


class DataAccessor:
    """Class to handle data access operations."""

    def __init__(self):
        self.engine = get_engine()

    def _get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def get_closest_providers_for_drg_cd(self, drg_cd: str, zip_code: str, radius_km: float = 10) -> list:
        """Get providers for a specific DRG code within a certain radius of a zip code."""

        latlong = get_gps_coordinates(zip_code)
        if not latlong:
            print(f"Could not get GPS coordinates for zip code: {zip_code}")
            return []

        lat, long = latlong

        session = self._get_session()
        try:
            point = WKTElement(f'POINT({long} {lat})', srid=4326)
            query = session.query(Provider).filter(
                Provider.drg_cd == drg_cd,
                Provider.location.ST_DWithin(point, radius_km * 1000)  # Convert km to meters
            )
            return query.all()
        finally:
            session.close()

    def get_closest_providers_for_drg_desc(self, drg_desc: str, zip_code: str, radius_km: float = 10) -> list[dict]:
        """Get providers for a specific DRG code within a certain radius of a zip code."""

        # Heuristic for max edits based on length (up to 25% of length)
        max_edits = max(1, len(drg_desc) // 4)

        latlong = get_gps_coordinates(zip_code)
        if not latlong:
            print(f"Could not get GPS coordinates for zip code: {zip_code}")
            return []

        lat, long = latlong

        session = self._get_session()
        try:
            point = WKTElement(f'POINT({long} {lat})', srid=4326)
            query = session.query(Provider).filter(
                Provider.drg_description.ilike(f"%{drg_desc}%"),
                Provider.location.ST_DWithin(point, radius_km * 1000)  # Convert km to meters
            )
            return [ object_as_dict(item) for item in query.all()]
        finally:
            session.close()

    def natural_language_to_sql_sqlalchemy(self, natural_language_query, db_schema_info) -> str:
        prompt = f"""
        You are an assistant that translates natural language questions into SQL queries for a database with the following schema:
        {db_schema_info}

        Translate the following natural language query into a SQL query:
        "{natural_language_query}"
        """

        response = openai.Completion.create(
            model="text-davinci-003", # Or a more recent model like gpt-4
            prompt=prompt,
            max_tokens=200,
            temperature=0
        )
        generated_sql: str = response.choices[0].text.strip()
        return generated_sql

    def execute_natural_language_query(self, natural_language_query: str) -> list[dict]:
        """Execute a natural language query against the database."""

        db_schema_info = Provider.__table__.schema

        sql_query = self.natural_language_to_sql_sqlalchemy(natural_language_query, db_schema_info)
        session = self._get_session()
        try:
            result = session.execute(sql_query)
            return [ object_as_dict(item) for item in result.fetchall()]
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
        finally:
            session.close()