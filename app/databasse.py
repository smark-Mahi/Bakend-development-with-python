from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# DATABASE_HOSTNAME = localhost
# DATABASE_PORT = 5433
# DATABASE_PASSWORD = mangu
# DATABASE_NAME = myfastapi
# DATABASE_USERNAME = postgres
# SCRET_KEY = hgfhgr67786g8o7987hug67565fhvnvczsdare67869867086765
# ALGORITHM = HS256
# ACCESS_TOKEN_EXPIRE_MINUTES == 30

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:mangu@localhost:5433/myfastapi"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()