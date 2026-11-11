# Day 3 — Backend Setup

范围：FastAPI、存活检查、PostgreSQL Compose、连接检查和环境配置。
今天不创建业务表，不实现登录或工单 API，也不自动执行建表。

## 1. 现有仓库核对

起点提交：`60e1089`。原仓库只有 README.md、docs/REQUIREMENTS.md 和
.gitignore，没有后端、前端或 Docker 配置。需求文档保持原样。
Day 2 对 Reopen 和历史记录的设计将在后续业务实现前整理，今天不改业务需求。

## 2. 准备环境（Windows PowerShell）

需要 Python 3.12+、Git，以及已启动且使用 Linux containers 的 Docker Desktop。
以下命令从仓库根目录执行。仅第一次、没有 .env 时复制样例：

```powershell
if (!(Test-Path .env)) { Copy-Item .env.example .env }
python -m venv backend/.venv
& ./backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
docker compose config --quiet
docker compose up -d --wait db
docker compose ps
```

`.env.example` 是可提交的本地开发样例；`.env` 已被原有 .gitignore 忽略。
数据库密码只适合本机开发。API 与 Compose 读取根目录的同一份 .env。
API 运行在 Windows，数据库端口只绑定本机，所以主机为 `127.0.0.1`。
未来若 API 也放入 Compose，主机需要改成服务名 `db`。

## 3. 启动 API

```powershell
Set-Location backend
& ./.venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

在第二个终端执行：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/health/db
```

打开 http://127.0.0.1:8000/docs 查看交互文档。

| 地址 | 验证什么 | 成功结果 |
| --- | --- | --- |
| `/health` | API 进程能响应 | 200，`{"status":"ok"}` |
| `/docs` | Swagger 文档页面 | 200，HTML |
| `/health/db` | SQLAlchemy + psycopg 对 PostgreSQL 执行 SELECT 1 | 200，`{"status":"ok","database":"ok"}` |

数据库不可用时 `/health/db` 返回 503，不暴露连接细节；`/health` 仍返回 200。
配置会在启动时验证，但数据库连接在探针被调用时才建立。
SQLAlchemy Engine 管理连接池，退出时释放；今天不需要业务 Session 或 ORM models。
URL.create 单独处理用户名与密码，避免密码中的 @、/ 等字符破坏连接字符串。

## 4. 测试与排查

在 backend 目录执行：

```powershell
& ./.venv/Scripts/python.exe -m pytest -q
```

测试覆盖存活检查、文档、数据库探针成功/失败响应以及密码特殊字符。
探针成功单元测试使用模拟；只有真实 `/health/db` 的 200 才证明 PostgreSQL 已连通。

如果数据库返回 503：先检查 Docker Desktop，再运行 `docker compose ps` 和
`docker compose logs --tail 50 db`（从根目录执行）。端口冲突时修改 .env 的
POSTGRES_PORT 并重新创建容器。数据库初始化变量仅在空数据卷时生效；
已有数据卷时修改 .env 密码不会自动更改数据库密码。

停止数据库可运行 `docker compose stop db`；命名数据卷会保留数据。

## 5. 8 个开发日的节奏

每天 4–6 小时，Day 3–10 共 32–48 小时。

| 开发日 | 重点 |
| --- | --- |
| Day 3 | 后端基础与真实数据库连接验收 |
| Day 4 | 最小数据模型、迁移、登录与权限 |
| Day 5 | 工单创建、列表、详情与编辑 |
| Day 6 | 分配、完成、重新打开与历史记录 |
| Day 7 | React 基础、路由与登录对接 |
| Day 8 | Dispatcher 核心页面 |
| Day 9 | Technician 核心页面 |
| Day 10 | 端到端验证、部署和演示文档 |

Day 3 验收通过后才进入业务实现；后续每天以能演示的核心流程作为交付标准。

## 6. 首轮验证（2026-11-11，重启前）

- 使用本机应用附带的 Python 3.12.14 建立 backend/.venv，运行依赖已安装。
  系统 `python` 目前是不可用的 Windows Store 别名。
- 在当前机器可直接从 backend 目录运行 `./.venv/Scripts/python.exe`，
  无需先激活环境，也不依赖系统 `python` 命令。
- `python -m pytest -q`：4 passed；有一条上游 Starlette TestClient
  对 httpx 的弃用提示，不影响本轮测试。
- 真实启动 Uvicorn 后发送 HTTP 请求：`/health` 200、`/docs` 200、
  `/health/db` 503，响应为 Database unavailable。验证后已停止临时服务。
- 初次检查没有 Docker。经用户授权，已安装 Docker Desktop 4.99.0、
  Docker CLI 29.9.3、Compose 5.7.0 和 WSL 3.0.5.0，
  并以管理员身份执行 `wsl --install --no-distribution`，退出码为 0。
- 使用安装目录中的 Compose 执行 `config --quiet`，退出码为 0。
- 系统显示待重启；WSL 状态提示虚拟化运行条件尚不可用。因此没有启动
  PostgreSQL 容器，也没有完成数据库成功连接验收。
  当时 Day 3 为部分完成；重启后验收结果见第 8 节。
- .env 与 backend/.venv 已确认被 Git 忽略；本轮没有提交或推送远程仓库。

主要实现依据：[FastAPI 入门](https://fastapi.tiangolo.com/tutorial/first-steps/)、
[SQLAlchemy Engine 与 URL](https://docs.sqlalchemy.org/en/20/core/engines.html)、
[PostgreSQL 官方镜像](https://hub.docker.com/_/postgres)。

## 7. 重启后操作步骤（现已完成）

1. 保存其他工作后手动重启 Windows，打开 Docker Desktop，等待引擎就绪。
2. 打开新的 PowerShell，在仓库根目录执行 `docker compose up -d --wait db`。
3. 按第 3 节启动 API，确认 `/health/db` 返回 200。
4. 若 WSL 仍提示虚拟化不可用，再检查 Windows 虚拟机平台和 BIOS/UEFI
   虚拟化设置；目前没有修改固件，也没有自动重启电脑。

如果新终端仍不识别 `docker compose`，可先使用安装目录中的 Compose：

```powershell
& 'C:/Program Files/Docker/Docker/resources/cli-plugins/docker-compose.exe' config --quiet
& 'C:/Program Files/Docker/Docker/resources/cli-plugins/docker-compose.exe' up -d --wait db
```

Windows 运行条件参考：[Docker Desktop Windows 安装说明](https://docs.docker.com/desktop/setup/install/windows-install/)、
[Microsoft WSL 安装与命令](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)。

## 8. 最终验收（2026-11-11，重启后）

**Day 3 Backend Setup 已通过本地验收。**

| 验收项 | 实际结果 |
| --- | --- |
| Docker 引擎 | 29.9.3，连接正常 |
| Compose 配置校验 | 通过 |
| PostgreSQL | 17.11，容器 fieldflow-db-1 为 Healthy |
| 数据库端口 | 仅绑定 127.0.0.1:5432 |
| Uvicorn 启动 | 成功 |
| GET /health | 200，`{"status":"ok"}` |
| GET /docs | 200，Swagger HTML |
| GET /openapi.json | 200，FieldFlow API 定义 |
| GET /health/db | 200，`{"status":"ok","database":"ok"}` |
| 自动化测试 | 4 passed；上游 TestClient 弃用提示仍存在 |
| 依赖检查 | No broken requirements found |
| public 中业务表数量 | 0，未创建业务 schema |

数据库健康接口本次使用真实连接，通过 SQLAlchemy + psycopg 执行 SELECT 1，
不是模拟测试结果。另通过容器内 psql 确认数据库名称为 fieldflow。

验收结束后 PostgreSQL 容器保持运行，临时 Uvicorn 服务已停止。
再次启动 API 可在 backend 目录运行：

```powershell
& ./.venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

本轮没有提交或推送 GitHub。下一阶段为 Day 4：先整理最小模型与状态约束，
再逐步加入迁移和认证，不在 Day 3 一次性生成全部业务 API。
