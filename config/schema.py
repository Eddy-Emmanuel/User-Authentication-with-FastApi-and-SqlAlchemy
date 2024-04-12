from pydantic import BaseModel

class Registration_Form(BaseModel):
    username : str 
    email: str
    password : str

class UserCreationResponse(BaseModel):
    message: str
    details: str
    
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token : str
    token_type : str
    
class UserDetails(BaseModel):
    username : str
    email :  str
    
class DeleteResponse(BaseModel):
    message : str