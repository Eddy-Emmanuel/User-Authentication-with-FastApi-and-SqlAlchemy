import sys
sys.path.append("./")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from config.configuration import CONFIGURATION

# Load Configurations
settings = CONFIGURATION()

# Create Engine
engine = create_engine(url=settings.ENGINE_URL, connect_args={"check_same_thread":False})

# Create Session
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = Session()
    try: 
        yield db
    finally:
        db.close()