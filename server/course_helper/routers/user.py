import re
import time

import requests

from fastapi import APIRouter, HTTPException
from lxml import etree
from pydantic import BaseModel
from requests import Session

from ..xmu_slider import xmu_slider_code
from ..common import success_info, CourseHelperException, error_info
from ..logger import Logger
from ..routers.websocket import ConnectionManager

router = APIRouter()
logger: Logger


class LoginModel(BaseModel):
    user_id: str
    user_pw: str
    vpn_id: str
    vpn_pw: str


class User:
    login_flag: bool = False
    login_model: LoginModel = None
    session: requests.Session = None

    @classmethod
    async def get_login_session(cls) -> requests.Session:
        # 需要检查登录状态是否有效
        if cls.login_flag:
            if not cls.check_login():
                # 登录状态已退出则重新登录
                logger.debug('登录状态异常, 重新登录')
                await course_login(cls.session, cls.login_model)
            return cls.session
        else:
            raise CourseHelperException('用户未登录')

    @classmethod
    async def get_session(cls) -> requests.Session:
        if cls.session is None:
            return cls.reset_session()
        return cls.session

    @classmethod
    def reset_session(cls):
        cls.session = requests.Session()
        cls.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/101.0.4951.54 Safari/537.36 '
        }
        return cls.session

    @classmethod
    def check_login(cls) -> bool:
        session = cls.session
        url = 'https://course.xmu.edu.cn/meol/oauth/callback.jsp'
        res = session.get(url=url)
        return res.url.find('main.jsp') > -1


@router.on_event("startup")
async def __init():
    #   获取默认日志
    global logger
    logger = Logger('用户模块')


@router.post("/login")
async def login(data: LoginModel):
    try:
        session = await User.get_session()
        await course_login(session, data=data)

        User.login_flag = True
        User.login_model = data

        user_info = get_user_info(session)
        return success_info(msg='登录成功！', data=user_info)
    except CourseHelperException as e:
        logger.warning(f'登录失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'登录失败 e-{e}')
        raise HTTPException(400, detail=error_info('登录失败'))


@router.get("/logout")
async def logout():
    try:
        url = 'https://course2.xmu.edu.cn/meol/ext/xmu/logout.jsp'
        (await User.get_session()).get(url=url)

        # course的退出不能将统一身份、vpn的退出，所以这里重置session
        User.reset_session()
        User.login_flag = False
        User.login_model = None
        return success_info(msg='已退出登录')

    except Exception as e:
        logger.debug(f'退出失败 e-{e}')
        raise HTTPException(400, detail=error_info('退出失败'))


async def course_login(session: requests.Session, data: LoginModel):
    url = 'https://course.xmu.edu.cn/meol/oauth/callback.jsp'
    res = session.get(url=url)
    if res.url.find('main.jsp') == -1:
        if res.url.find('authserver') > -1:
            # 统一身份登录
            res = await login_by_ids(session, data.user_id, data.user_pw, login_url=res.url)
            logger.debug('统一身份登录成功')

        if res.url.find('wengine-auth') > -1:
            # vpn登录
            res = await login_vpn(session, data.vpn_id, data.vpn_pw)
            logger.debug('VPN登录成功')

        if res.url.find('main.jsp') == -1:
            raise CourseHelperException('Course平台进入失败')


async def login_vpn(session: requests.Session, account: str, pw: str) -> requests.Response:
    base_url = 'https://applg.xmu.edu.cn/wengine-auth/'

    # 获取滑块验证码 延迟0.5s避免请求502
    time.sleep(0.5)
    img_res = session.get(url=base_url + 'login/image')
    if img_res.status_code != 200:
        raise CourseHelperException('滑块验证码加载失败')

    w = xmu_slider_code(img_res.json()['p'])

    # 验证验证码
    data = {
        'w': w,
        't': 0,
        'locations': [{'x': 156, 'y': 572}, {'x': 156 + w, 'y': 479}]  # 数字不重要，关键是 w
    }
    code_res = session.post(url=base_url + 'login/verify', data=data)
    if code_res.status_code != 200 or not code_res.json()['success']:
        raise CourseHelperException('滑块验证码验证失败')

    # 登录
    login_res = session.post(url=base_url + 'do-login', data={
        'auth_type': 'local',
        'username': account,
        'sms_code': '',
        'password': pw
    })

    login_res_json = login_res.json()
    if 'success' in login_res_json and login_res_json['success'] is True:
        return session.get(url=login_res_json['url'])
    else:
        if 'message' in login_res_json:
            raise CourseHelperException(f"vpn登录失败: {login_res_json['message']}")
        else:
            raise CourseHelperException('vpn登录失败')


async def login_by_ids(session: requests.Session, account: str, pw: str, login_url: str) -> requests.Response:
    """
    通过账号密码登录
    :param login_url: 登录链接, 方便跳转
    :param session: requests.Session
    :param account: 账号
    :param pw: 密码
    :return: 统一身份登录响应
    """
    if not len(ConnectionManager.active_connections):
        raise CourseHelperException('未连接客户端')

    res = session.get(login_url, timeout=5)
    if res.status_code != 200:
        raise CourseHelperException('统一身份登录网页加载失败')

    info = {}
    for name in ('lt', 'dllt', 'execution', '_eventId', 'rmShown', 'pwdDefaultEncryptSalt'):
        key = 'name' if name != 'pwdDefaultEncryptSalt' else 'id'
        result = re.search(r'{}="{}" value="([\s\S]*?)"'.format(key, name), res.text)
        if result is None:
            raise CourseHelperException('正则获取统一身份登录网页参数失败')
        info[name] = result.group(1)

    #   调用前端执行js加密代码
    res = await ConnectionManager.Utils.js_encrypt({
        'data': pw,
        'key': info['pwdDefaultEncryptSalt']
    }, client_id=tuple(ConnectionManager.active_connections.keys())[0])
    password = res['data']

    # 登录
    data = {
        'username': account,
        'password': password,
        'lt': info['lt'],
        'dllt': info['dllt'],
        'execution': info['execution'],
        '_eventId': info['_eventId'],
        'rmShown': info['rmShown']
    }

    login_res = session.post(login_url, data=data)
    if login_res.status_code != 200 or login_res.text.find('您提供的用户名或者密码有误') > -1 or login_res.text.find('请输入验证码') > -1:
        raise CourseHelperException('统一身份登录失败')
    return login_res


def get_user_info(s: Session) -> dict:
    res = s.get('https://course2.xmu.edu.cn/meol/popups/viewstudent_info.jsp?SID=224501&from=welcomepage')
    html = etree.HTML(res.text)
    table = html.xpath("//table[@class='infotable']")[0]
    result = [x.text.strip() for x in table.xpath("//td")]
    return {
        'id': result[1],
        'name': result[2],
        'college': result[3]
    }
