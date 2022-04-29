from fastapi import FastAPI

# 添加项目路径进入环境变量，避免找不到模块
import sys
import os

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from course_helper.routers import user, websocket

app = FastAPI()


@app.on_event("startup")
async def __init():
    # WebSocket路由
    app.include_router(websocket.router, prefix="/websocket")
    # 用户路由
    app.include_router(user.router, prefix="/user")


@app.get('/')
async def hello_world():
    return 'Hello world'


if __name__ == "__main__":
    import uvicorn

    # noinspection PyTypeChecker
    uvicorn.run(app, host='127.0.0.1', port=6498)
