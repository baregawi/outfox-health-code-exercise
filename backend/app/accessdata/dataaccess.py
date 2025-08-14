from datatypes import Base

from sqlalchemy import create_engine, Engine


DB_USER = "postgres"
DB_PASSWORD = "buruk101"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "outfoxhealth"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def setup_database() -> Engine:
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