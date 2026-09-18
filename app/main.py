from __future__ import annotations

import time
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.models import Task, store

app = FastAPI(title="AiToEarn", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

store.seed()


class ClaimBody(BaseModel):
    userId: str
    taskId: str


class SubmitBody(BaseModel):
    userId: str
    taskId: str
    result: str


@app.on_event("startup")
def _seed() -> None:
    store.seed()


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/api/tasks")
def list_tasks(category: str | None = None, status: str | None = None) -> list[dict]:
    tasks = list(store.tasks.values())
    if category:
        tasks = [t for t in tasks if t.category == category]
    if status:
        tasks = [t for t in tasks if t.status == status]
    return [store.public_task(t) for t in tasks]


@app.post("/api/tasks/claim")
def claim(body: ClaimBody) -> dict:
    task = store.tasks.get(body.taskId)
    if task is None:
        raise HTTPException(404, "task not found")
    if task.status != "open":
        raise HTTPException(409, "task already claimed")
    if body.userId not in store.users:
        raise HTTPException(404, "user not found")
    task.status = "in_progress"
    task.assignee = body.userId
    return store.public_task(task)


@app.post("/api/tasks/submit")
def submit(body: SubmitBody) -> dict:
    task = store.tasks.get(body.taskId)
    if task is None:
        raise HTTPException(404, "task not found")
    if task.status != "in_progress" or task.assignee != body.userId:
        raise HTTPException(409, "task not claimable by this user")
    if not body.result or len(body.result.strip()) < 3:
        raise HTTPException(400, "result too short")
    task.status = "submitted"
    return store.public_task(task)


@app.post("/api/tasks/{task_id}/approve")
def approve(task_id: str) -> dict:
    task = store.tasks.get(task_id)
    if task is None:
        raise HTTPException(404, "task not found")
    if task.status != "submitted":
        raise HTTPException(409, "task not in submitted state")
    task.status = "paid"
    user = store.users.get(task.assignee or "")
    if user is not None:
        user.balance += task.reward
    return {**store.public_task(task), "paidTo": task.assignee, "reward": task.reward}


@app.get("/api/users/{user_id}")
def user_detail(user_id: str) -> dict:
    user = store.users.get(user_id)
    if user is None:
        raise HTTPException(404, "user not found")
    done = [t.id for t in store.tasks.values() if t.assignee == user_id and t.status == "paid"]
    return {"id": user.id, "name": user.name, "balance": user.balance, "doneTasks": done}


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
