from fastapi import APIRouter, Depends, HTTPException
from db import session
from db.session import SessionLocal
from models.project import Project
from schema.user import  User

from core.security import get_current_user
from schema.project import ProjectCreate, ProjectResponse
from service.github_service import GithubManager
from core.config import settings


router = APIRouter(prefix="/project")
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()



@router.get("/",  status_code=200)
def getprojects(response_model: list[ProjectResponse], current_user: User = Depends(get_current_user), db: session = Depends(get_db))-> list[ProjectResponse]:
    projects: list[ProjectResponse]=db.query(Project).filter(Project.owner_id == current_user.id).all()
    if projects is None:
        raise HTTPException(status_code=404, detail="Project not found")
    print ("were in project")
    return projects
@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    project_data: ProjectCreate,  
    current_user: User = Depends(get_current_user),
    db: session = Depends(get_db),
):
    new_project = Project(**project_data.dict(), owner_id=current_user.id)
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

  
    return ProjectResponse.model_validate(new_project)

@router.get("/trjim/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, current_user: User = Depends(get_current_user), db: session = Depends(get_db)):
  
    project = db.query(Project).filter(Project.id == project_id).first()

    if project is None or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        repo_parts = project.repo_url.rstrip("/").split("/")[-2:]
        repo_owner, repo_name = repo_parts
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repository URL format.")

    forked_repo_name = GithubManager.fork_repo(repo_owner, repo_name)
    if not forked_repo_name:
        raise HTTPException(status_code=500, detail="Failed to fork repository.")

  
    username, repo_name = forked_repo_name.split("/")
    local_path = await GithubManager.clone_repo(username, repo_name)
    if not local_path:
        raise HTTPException(status_code=500, detail="Failed to clone repository.")
    #call the model

    await GithubManager.push_repo(local_path)

    pr_url = await GithubManager.create_pull_request(settings.GITHUB_ACCESS_TOKEN, username, repo_owner, repo_name)
    if not pr_url:
        raise HTTPException(status_code=500, detail="Failed to create pull request.")

    project.pr_url = pr_url

    return project
    
    
    