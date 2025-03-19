from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    id : int
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
