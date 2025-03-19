from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db.session import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    repo_url = Column(String, nullable=False)
    description = Column(String)
    language = Column(JSON, default=[])  
    directory = Column(JSON, default=[]) 
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", backref="projects")
