import sys
sys.path.append("./")

from database.create_session import Base

from sqlalchemy import Integer, String, Column

class DataBaseTable(Base):
    __tablename__ = "databasetable"
    
    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

