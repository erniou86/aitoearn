from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    id: str
    title: str
    description: str
    reward: float
    category: str
    status: str = "open"  # open / in_progress / submitted / paid
    created_at: float = field(default_factory=time.time)
    assignee: Optional[str] = None


@dataclass
class User:
    id: str
    name: str
    balance: float = 0.0


class Store:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}
        self.users: dict[str, User] = {}

    def seed(self) -> None:
        demo = [
            ("t1", "标注图片中的车辆类别", "给 50 张街景图片标注车辆类型（轿车/卡车/摩托）", 2.5, "data"),
            ("t2", "撰写产品文案 100 字", "为智能水杯写一段 100 字电商卖点文案", 1.8, "content"),
            ("t3", "收集 20 条中文谚语", "整理常用谚语并给出释义，JSON 格式输出", 3.0, "data"),
            ("t4", "AI 对话质量打分", "对 30 组对话按 helpfulness 打分并给出理由", 4.0, "eval"),
        ]
        for tid, title, desc, reward, cat in demo:
            self.tasks[tid] = Task(id=tid, title=title, description=desc, reward=reward, category=cat)
        self.users["u1"] = User(id="u1", name="demo-user")

    def public_task(self, t: Task) -> dict:
        return {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "reward": t.reward,
            "category": t.category,
            "status": t.status,
        }


store = Store()
