from fastapi import APIRouter, HTTPException
from lxml import etree
from pydantic import BaseModel

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


@router.get('/getCourseList')
async def get_course_list():
    """
    获取基本信息
    用户基本信息、课程列表
    """
    try:
        session = await User.get_login_session()
        res = session.get('https://course2.xmu.edu.cn/meol/lesson/blen.student.lesson.list.jsp')
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
        return success_info(msg='获取课程列表成功！', data=course_list)

    except CourseHelperException as e:
        logger.warning(f'获取课程列表失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'获取课程列表失败 e-{e}')
        raise HTTPException(400, detail=error_info('获取课程列表失败'))


@router.get('/getCourseIntroduction/{course_id}')
async def get_course_introduction(course_id: str):
    """
    获取课程介绍
    """
    try:
        session = await User.get_login_session()
        res = session.get(f'https://course2.xmu.edu.cn/meol/lesson/coursesum.jsp?lid={course_id}')
        html = etree.HTML(res.text)
        nodes = html.xpath("//td[@class='text']//input[@type='hidden']")
        content = nodes[0].attrib['value']
        return success_info(msg='获取课程介绍成功', data={
            'course_id': course_id,
            'content': content
        })

    except CourseHelperException as e:
        logger.warning(f'获取课程介绍失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'获取课程介绍失败 e-{e}')
        raise HTTPException(400, detail=error_info('获取课程介绍失败'))


@router.get('/getCourseHomework/{course_id}')
async def get_course_homework(course_id: str):
    """
    获取课程作业
    """
    try:
        session = await User.get_login_session()
        session.get(f'https://course2.xmu.edu.cn/meol/jpk/course/layout/newpage/index.jsp?courseId={course_id}')
        res = session.get('https://course2.xmu.edu.cn/meol/common/hw/student/hwtask.jsp')
        html = etree.HTML(res.text)
        nodes: list = html.xpath("//table[@class='valuelist']//tr")
        nodes.pop(0)

        homeworks = []
        for node in nodes:
            cols = node.xpath("./td")
            ele_a = cols[0].xpath("./a[1]")[0]
            hw_obj = {
                'hw_id': ele_a.attrib['href'][ele_a.attrib['href'].find('=') + 1:],
                'title': ele_a.text.strip()
            }

            for index, name in enumerate(['end_data', 'score', 'publisher'], 1):
                hw_obj[name] = cols[index].text.strip()

            #   超时或已提交则为false
            hw_obj['committable'] = len(cols[5].xpath('./a')) > 0
            homeworks.append(hw_obj)

        return success_info(msg='获取课程作业成功', data={
            'course_id': course_id,
            'homeworks': homeworks
        })

    except CourseHelperException as e:
        logger.warning(f'获取课程作业失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'获取课程作业失败 e-{e}')
        raise HTTPException(400, detail=error_info('获取课程作业失败'))


@router.get('/getHomeworkDetails/{hw_id}')
async def get_homework_details(hw_id: str):
    try:
        session = await User.get_login_session()
        res = session.get(f'https://course2.xmu.edu.cn/meol/common/hw/student/taskanswer.jsp?hwtid={hw_id}')
        html = etree.HTML(res.text)

        content = {}
        tables = html.xpath("//table[@class='infotable']")

        for index, name in enumerate(['title', 'end_data', 'scoring_method', 'score'], 1):
            content[name] = tables[0].xpath(f".//tr[{index}]/td")[0].text.strip()

        nodes = (
            tables[0].xpath(".//tr[5]/td/input"),
            tables[1].xpath('.//tr[2]/td/input'),
            tables[2].xpath('.//tr[2]/td/input'),
        )
        names = ('content', 'answer', 'result', 'comment')

        for index in range(3):
            content[names[index]] = nodes[index][0].attrib['value'] if len(nodes[index]) > 0 else ''
        content['comment'] = tables[3].xpath('.//tr[2]/td')[0].text.strip()

        return success_info(msg='获取课程作业成功', data={
            'hw_id': hw_id,
            'content': content
        })

    except CourseHelperException as e:
        logger.warning(f'获取作业详情失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'获取作业详情失败 e-{e}')
        raise HTTPException(400, detail=error_info('获取课程详情失败'))


class T(BaseModel):
    url: str


@router.post('/getTest')
async def test(t: T):
    s = await User.get_login_session()
    res = s.get(url=t.url)
    return res.text
