from fastapi import APIRouter, HTTPException
from requests import Session
from lxml import etree

from .user import User
from ..common import success_info, CourseHelperException, error_info
from ..logger import Logger

router = APIRouter()
logger: Logger


@router.on_event("startup")
async def __init():
    #   获取默认日志
    global logger
    logger = Logger('课程模块')


@router.get('/getBasicInfo')
async def get_basic_info():
    """
    获取基本信息
    用户基本信息、课程列表
    """
    try:
        session = await User.get_login_session()
        user_info = get_user_info(session)
        course_list = get_course_list(session)
        return success_info(msg='获取成功！', data={
            'user_info': user_info,
            'course_list': course_list
        })

    except CourseHelperException as e:
        logger.warning(f'获取基本信息失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'获取基本信息失败 e-{e}')
        raise HTTPException(400, detail=error_info('获取基本信息失败'))


def get_user_info(s: Session):
    res = s.get('https://course2.xmu.edu.cn/meol/popups/viewstudent_info.jsp?SID=224501&from=welcomepage')
    html = etree.HTML(res.text)
    table = html.xpath("//table[@class='infotable']")[0]
    result = [x.text.strip() for x in table.xpath("//td")]
    return {
        'id': result[1],
        'name': result[2],
        'college': result[3]
    }


def get_course_list(s: Session):
    res = s.get('https://course2.xmu.edu.cn/meol/lesson/blen.student.lesson.list.jsp')
    html = etree.HTML(res.text)
    tr_list = html.xpath("//table[@id='table2']//tr")
    tr_list.pop(0)

    course_list = []
    for tr in tr_list:
        td_list = tr.xpath('.//td')

        a = td_list[0].xpath('./a')[0]
        href = a.attrib['href']
        course_list.append({
            'name': a.text.strip(),
            'college': td_list[1].text.strip(),
            'teacher': td_list[2].text.strip(),
            'course_id': href[href.find('?lid=') + 5:]
        })

    return course_list
