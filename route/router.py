import sys
sys.path.append("./")

from database.create_session import get_db
from database.create_table import DataBaseTable
from service.backend_service import password_hasher
from service.backend_service import SERVICE, password_hasher
from config.schema import UserCreationResponse, Token, Registration_Form, UserDetails, DeleteResponse

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

USER_ROUTER = APIRouter(tags=["User"])
AUTH_ROUTER = APIRouter(tags=["Auth"])

oauthpasswordbearer = OAuth2PasswordBearer(tokenUrl="/authenticate_user")

@USER_ROUTER.post("/register_user", response_model=UserCreationResponse)
async def RegisterUser(data : Registration_Form, db:Session=Depends(get_db)):
    service = SERVICE(username=data.username, email=data.email, db=db, password=data.password)
    try:
        # Check if user already in database
        filtuser = await service.GetUserFromDB()
        
        # Create new database for user that is not already registered
        if not filtuser:
            new_user = DataBaseTable(username = data.username,
                                     email = data.email,
                                     hashed_password = password_hasher.hash(data.password))
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return JSONResponse(content={"message":"User successfully created", "details":f"id:{new_user.id}, username:{new_user.username}, email:{new_user.email}"})
        
        else:
            raise HTTPException(status_code=400, detail="User already exists")
        
    except Exception:
        # Handle any unexpected errors and return an appropriate response
        raise HTTPException(status_code=500, detail=str(Exception))
    
    
@AUTH_ROUTER.post("/authenticate_user", response_model=Token)
async def GetAccessToken(data: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    service = SERVICE(username=data.username, db=db, password=data.password)
    access_token = await service.GetAccessToken()
    return access_token
  
    
@USER_ROUTER.get("/get_user", response_model=UserDetails)
async def GetUser(token:DataBaseTable=Depends(oauthpasswordbearer), db:Session=Depends(get_db)):
    service = SERVICE()
    userdata = await service.VerifyUser(token=token, db=db)
    return {"username":userdata.username, "email":userdata.email}
    
@USER_ROUTER.delete("/delete_user", response_model=DeleteResponse)
async def DeleteUser(token:Annotated[str, Depends(oauthpasswordbearer)], db:Annotated[Session, Depends(get_db)]):
    # db:Annotated[Session, Depends(get_db)] is same as db:Session=Depends(get_db)
    service = SERVICE()
    return await service.DELETE_CURRENT_USER(token=token, db=db)