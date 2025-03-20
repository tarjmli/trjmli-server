from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ProjectBase(BaseModel):
    name: str
    repo_url: HttpUrl
    description: Optional[str] = None
    language: List[str] 
    directory: List[str] = []
    

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
 

    class Config:
        from_attributes = True
