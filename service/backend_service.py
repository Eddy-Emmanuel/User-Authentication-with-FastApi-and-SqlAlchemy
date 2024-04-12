import sys
sys.path.append("./")

from config.configuration import CONFIGURATION
from database.create_table import DataBaseTable

from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, datetime
from fastapi import HTTPException, status

CONFIG = CONFIGURATION()
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SERVICE:
    
    def __init__(self, username:str=None, password:str=None, db:Session=None, email:str=None):
        self.username = username
        self.email = email
        self.password = password
        self.db = db
    
    # Get User from database
    async def GetUserFromDB(self):
        filteruser = self.db.query(DataBaseTable).filter(DataBaseTable.username == self.username, DataBaseTable.email == self.email).first()
        return filteruser
    
    # Get access token
    async def GetAccessToken(self):
        FilterUser = self.db.query(DataBaseTable).filter(DataBaseTable.username == self.username).first()
        
        if not FilterUser:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Username/Email not found in database", 
                                headers={"WWW-Authenticate":"Bearer"})
            
        if not password_hasher.verify(secret=self.password, hash=FilterUser.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Incorrect Password", 
                                headers={"WWW-Authenticate":"Bearer"})
            
        data = {"user_id": FilterUser.id,
                "username": FilterUser.username,
                "exp_time":str(datetime.utcnow() + timedelta(minutes=CONFIG.TOKEN_EXPIRE_TIME))}
        
        return {"access_token": jwt.encode(data, CONFIG.SECRET_KEY, algorithm=CONFIG.ALGORITHM), "token_type":"bearer"}
    
    # Verify User 
    async def VerifyUser(self, token:str, db:Session):
        try:
            decoded_hashed_password = jwt.decode(token, CONFIG.SECRET_KEY, algorithms=CONFIG.ALGORITHM)
            userid = decoded_hashed_password.get("user_id", None)
            username = decoded_hashed_password.get("username", None)
            
            if (userid is None) and (username is None):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could Not Validate User")
            
            # Get User Details
            return db.query(DataBaseTable).filter(DataBaseTable.username == username, DataBaseTable.id == userid).first()
                
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
        
    # Delete Current User
    async def DELETE_CURRENT_USER(self, token:str, db:Session):
        try:
            decoded_token = jwt.decode(token, CONFIG.SECRET_KEY, algorithms=CONFIG.ALGORITHM)
            username = decoded_token.get("username", None)
            userid = decoded_token.get("user_id", None)
            
            if (username is None) or (userid is None):
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No such user in our database")
            
            db.query(DataBaseTable).filter(DataBaseTable.username == username, DataBaseTable.id == userid).delete()
            db.commit()  
            return {"message": "User deleted successfully"}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            
        
    
    
        
    