# AiToEarn

开源 AI 众包任务平台：发布数据标注 / 内容创作 / AI 评测任务，接单完成后获得 ETH 奖励。
**适用人群**：需要众包 AI 数据标注与内容创作的团队、Web3 项目方，以及想通过完成任务赚取 ETH 报酬的接单用户。

## 功能特性

- 任务大厅（分类筛选、状态徽章）
- 领取 → 提交 → 审核 → 放款全流程
- 用户余额与完成记录
- 内置响应式前端（零构建）

## 技术栈与目录结构

**技术栈**：Python / FastAPI / Pydantic / Uvicorn / pytest

```
aitoearn/
├── app/
│   ├── main.py        # FastAPI 入口（任务众包 API）
│   └── models.py      # Pydantic 模型
├── tests/
│   └── test_api.py    # 单元测试（pytest）
├── frontend/
│   └── index.html     # 零构建响应式前端
├── requirements.txt
└── Dockerfile
```

## 快速开始

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000

# 运行测试
pytest -q
```

**Docker 部署**

```bash
docker build -t aitoearn .
docker run -p 8000:8000 aitoearn
```

**部署说明**：标准 FastAPI 应用，可部署到任意支持 Python 3.11+ 的平台（VPS / Docker / Render / Railway 等）；当前为内存存储，生产环境可扩展接入 PostgreSQL。

## 验证状态

引用 AI Factory 全套件验证报告（[VERIFICATION.md](../../VERIFICATION.md)，2026-09-18，Windows 11 / Python 3.11.8），本机已完成运行验证：

- `python -m pytest tests/test_api.py -q`：**5 passed**（health、任务领取、提交、审核放款全流程）
- 栈：FastAPI + Pydantic + 内存存储；前端 frontend/index.html

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/tasks?category=&status=` | 任务列表 |
| POST | `/api/tasks/claim` | 领取任务 `{userId, taskId}` |
| POST | `/api/tasks/submit` | 提交结果 `{userId, taskId, result}` |
| POST | `/api/tasks/:id/approve` | 审核通过并放款 |
| GET | `/api/users/:id` | 用户余额 / 完成记录 |

## License

MIT License，详见 [LICENSE](LICENSE)。本项目代码与文档由 AI 辅助生成，仅供参考与学习使用。

## 支持项目

如果这个项目对你有帮助，欢迎赞助支持持续开发：

[![PayPal](https://img.shields.io/badge/Donate-PayPal-00457C?style=flat-square&logo=paypal)](https://paypal.me/Junlong439)
