# AiToEarn

开源 AI 众包任务平台：发布数据标注 / 内容创作 / AI 评测任务，接单完成后获得 ETH 奖励。

## 功能
- 任务大厅（分类筛选、状态徽章）
- 领取 → 提交 → 审核 → 放款全流程
- 用户余额与完成记录
- 内置响应式前端（零构建）

## 快速开始
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000
```

## 测试
```bash
pytest -q
```

## Docker
```bash
docker build -t aitoearn .
docker run -p 8000:8000 aitoearn
```

## API
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/tasks?category=&status=` | 任务列表 |
| POST | `/api/tasks/claim` | 领取任务 `{userId, taskId}` |
| POST | `/api/tasks/submit` | 提交结果 `{userId, taskId, result}` |
| POST | `/api/tasks/:id/approve` | 审核通过并放款 |
| GET | `/api/users/:id` | 用户余额 / 完成记录 |

## License
MIT
