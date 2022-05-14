import asyncio
import json
import time
from json import JSONDecodeError

import nanoid
from fastapi import APIRouter, WebSocket

from course_helper.logger import Logger

router = APIRouter()
logger: Logger


class ConnectionManager:
    active_connections: dict = {}
    wait_reply_dict: dict = {}

    class Utils:
        @staticmethod
        async def js_encrypt(data: dict, client_id: str):
            """
            请求客户端 执行js 并返回结果
            """
            return await ConnectionManager.send_message_wait_reply({
                'cmd': 'js_encrypt',
                'params': data
            }, client_id)

    @classmethod
    async def connect(cls, ws: WebSocket, client_id: str):
        """
        等待连接，并添加连接对象
        """
        await ws.accept()
        cls.active_connections[client_id] = ws
        logger.info(f"WS已连接 client_id:{client_id}")

    @classmethod
    def disconnect(cls, client_id: str):
        """
        移除连接对象
        """
        cls.active_connections.pop(client_id)
        logger.info(f"WS已断开 client_id:{client_id}")

    @classmethod
    async def send_message(cls, data, client_id: str):
        """
        给某个连接发送消息
        """
        message_id = nanoid.generate()
        await cls.active_connections[client_id].send_text(json.dumps({
            'message_id': message_id,
            'data': data
        }))
        logger.debug(f"发送消息给 client_id:{client_id} | message_id:{message_id}")

    @classmethod
    async def send_message_wait_reply(cls, data, client_id: str):
        """
        给某个连接发送消息并等待回复
        """
        message_id = nanoid.generate()
        await cls.active_connections[client_id].send_text(json.dumps({
            'reply': True,
            'message_id': message_id,
            'data': data
        }))
        #   等待回复
        reply = await cls.wait_reply(message_id)
        cls.wait_reply_dict.pop(message_id)
        logger.debug(f"发送消息给 client_id:{client_id} message_id:{message_id}")

        return reply

    @classmethod
    async def wait_reply(cls, message_id: str):
        """
        等待指定message_id的回复
        """
        future = asyncio.Future()
        cls.wait_reply_dict[message_id] = future
        #   等待 future 结果，然后返回
        return await future

    @classmethod
    async def on_json_message(cls, message, client_id: str):
        """
        收到任何消息的触发函数
        """
        if isinstance(message, dict):
            logger.debug(f"收到消息 client_id:{client_id}")
            if 'reply' in message:
                # 存在回复
                for _ in range(3):
                    #  防止回复过快，future还未添加
                    if message['message_id'] in cls.wait_reply_dict:
                        future = cls.wait_reply_dict[message['message_id']]
                        #   设定future结果，从而结束 wait_reply
                        future.set_result(message)
                        break
                    else:
                        time.sleep(0.1)
        elif message == 'heartCheck':
            # logger.debug(f"收到心跳包")
            #   心跳包回复
            await ConnectionManager.active_connections[client_id].send_text('heartCheck')

        #   不满足条件的消息，不做处理


@router.on_event("startup")
async def __init():
    #   获取默认日志
    global logger
    logger = Logger('WebSocket模块')


@router.websocket("/connect/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    websocket连接
    """
    await ConnectionManager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            await ConnectionManager.on_json_message(data, client_id)

    except JSONDecodeError:
        logger.debug(f"收到 client_id:{client_id} 非json格式消息 已忽略")
    except:
        ConnectionManager.disconnect(client_id)
