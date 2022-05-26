import argparse
import signal

import psutil
from fastapi import FastAPI

import sys
import os

# 添加项目路径进入环境变量，避免找不到模块
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from starlette.middleware.cors import CORSMiddleware
from course_helper.routers import user, websocket, course

# 神奇地修复了CMD下颜色乱码的问题
os.system('')


def pid_lock():
    if os.path.exists('server.pid'):
        with open('server.pid') as f:
            pid = f.read()
            if psutil.pid_exists(int(pid)):
                sys.exit(0)
    with open('server.pid', 'w') as f:
        f.write(str(os.getpid()))


def close_server():
    if os.path.exists('server.pid'):
        with open('server.pid') as f:
            pid = f.read()
            # 虽然能结束进程，但是有莫名其妙的错误
            try:
                p = psutil.Process(int(pid))
                p.send_signal(signal.CTRL_C_EVENT)
            except:
                pass


# 命令行参数
parser = argparse.ArgumentParser(description='CourseHelper server!')
parser.add_argument('cmd', type=str, nargs='?', default='start', help='start (default), stop, restart')
args = parser.parse_args()

if args.cmd == 'stop':
    close_server()
    sys.exit(0)
elif args.cmd == 'restart':
    close_server()
    # 保证锁文件已清除
    if os.path.exists('server.pid'):
        os.remove('server.pid')

# 开启程序单实例锁
pid_lock()

app = FastAPI()

# 设置跨域传参
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 设置允许访问的域名 "*"，即为所有。
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"]  # 允许跨域的headers，可以用来鉴别来源等作用。
)


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
