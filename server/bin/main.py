from fastapi import FastAPI

# 添加项目路径进入环境变量，避免找不到模块
import sys
import os

from starlette.middleware.cors import CORSMiddleware

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from course_helper.routers import user, websocket, course

app = FastAPI()

# 设置允许访问的域名
origins = [
    '*'
]  # 也可以设置为"*"，即为所有。

# 设置跨域传参
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  # 允许跨域的headers，可以用来鉴别来源等作用。


@app.on_event("startup")
async def __init():
    # WebSocket路由
    app.include_router(websocket.router, prefix="/websocket")
    # 用户路由
    app.include_router(user.router, prefix="/user")
    # 课程路由
    app.include_router(course.router, prefix="/course")


@app.get('/')
async def hello_world():
    return 'Hello world'


if __name__ == "__main__":
    import uvicorn

    # noinspection PyTypeChecker
    uvicorn.run(app, host='127.0.0.1', port=6498)
