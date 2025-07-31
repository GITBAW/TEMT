from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Environment(BaseModel):
    id: str
    name: str
    type: str
    url: str
    status: str = "Available"
    booked_by: Optional[str] = None
    booked_from: Optional[str] = None
    booked_to: Optional[str] = None
    project: str

class Project(BaseModel):
    id: str
    name: str

environments = []
projects = []

def authorize(token: str = Header(...)):
    if token != "admin123":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/environments", response_model=List[Environment])
def list_envs(project: Optional[str] = None):
    return [env for env in environments if env["project"] == project] if project else environments

@app.post("/environments", response_model=Environment)
def add_env(env: Environment, token: str = Depends(authorize)):
    env.id = str(uuid4())
    environments.append(env.dict())
    return env

@app.put("/environments/{env_id}", response_model=Environment)
def update_env(env_id: str, updated: Environment, token: str = Depends(authorize)):
    for i, env in enumerate(environments):
        if env["id"] == env_id:
            environments[i] = updated.dict()
            return updated
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/projects", response_model=List[Project])
def list_projects():
    return projects

@app.post("/projects", response_model=Project)
def create_project(project: Project, token: str = Depends(authorize)):
    project.id = str(uuid4())
    projects.append(project.dict())
    return project