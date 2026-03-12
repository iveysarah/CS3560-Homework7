from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI(title="Production‑Style REST API", version="1.0.0")

users: Dict[int, dict] = {}
tasks: Dict[int, dict] = {}

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class TaskCreate(BaseModel):
    title: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


# GET
@app.get("/users", summary="Get all users")
def get_all_users():
    return users

@app.get("/tasks/{task_id}", summary="Get a specific task")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


# POST
@app.post("/users", status_code=201, summary="Create a new user")
def create_user(user: UserCreate):
    user_id = len(users) + 1
    users[user_id] = user.dict()
    return {"id": user_id, **users[user_id]}

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):
    task_id = len(tasks) + 1
    tasks[task_id] = task.dict()
    return {"id": task_id, **tasks[task_id]}


# PUT
@app.put("/users/{user_id}", summary="Replace a user")
def replace_user(user_id: int, user: UserCreate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = user.dict()
    return {"id": user_id, **users[user_id]}

@app.put("/tasks/{task_id}", summary="Replace a task")
def replace_task(task_id: int, task: TaskCreate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task.dict()
    return {"id": task_id, **tasks[task_id]}


# PATCH
@app.patch("/users/{user_id}", summary="Partially update a user")
def patch_user(user_id: int, user: UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    stored = users[user_id]
    update_data = user.dict(exclude_unset=True)
    stored.update(update_data)
    return {"id": user_id, **stored}

@app.patch("/tasks/{task_id}", summary="Partially update a task")
def patch_task(task_id: int, task: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    stored = tasks[task_id]
    update_data = task.dict(exclude_unset=True)
    stored.update(update_data)
    return {"id": task_id, **stored}


# DELETE
@app.delete("/users/{user_id}", status_code=204, summary="Delete a user")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return