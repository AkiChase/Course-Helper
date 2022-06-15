import os

from fastapi import APIRouter, HTTPException, BackgroundTasks, Response
from pydantic import BaseModel

from .user import User
from ..common import success_info, CourseHelperException, error_info
from ..logger import Logger
from ..download import Downloader

router = APIRouter()
logger: Logger


class DownloadModel(BaseModel):
    file_id: str
    dir_path: str


class UploadFileModel(BaseModel):
    file_path: str


@router.on_event("startup")
async def __init():
    #   获取默认日志
    global logger
    logger = Logger('文件模块')


@router.post('/downloadFile')
async def download_file(data: DownloadModel, background_tasks: BackgroundTasks):
    """
    下载course网站内openfile指向的文件
    """
    try:
        s = await User.get_login_session()
        r = s.get(f'https://course2.xmu.edu.cn/meol/common/ckeditor/openfile.jsp?id={data.file_id}', stream=True)
        file_size = int(r.headers['content-length'])  # 文件大小 Byte
        file_name = Downloader.get_headers_file_name(r.headers.get("Content-Disposition"))
        while True:
            # 拼接目录 子目录 文件名
            file_path = os.path.abspath(os.path.join(data.dir_path, file_name))
            if os.path.exists(file_path):
                # 文件名重复则添加一个#
                file_name_no_ext = file_name[0:file_name.rfind('.')]
                file_ext = file_name[file_name.rfind('.') + 1:]
                file_name = f"{file_name_no_ext}#.{file_ext}"
            else:
                break

        background_tasks.add_task(Downloader.download_open_in_folder, file_path, r)
        return success_info('开始下载！下载完成后将在文件夹显示', data={
            'file_name': file_name,
            'file_path': file_path,
            'file_size': Downloader.byte_to_suitable_size(file_size)
        })
    except CourseHelperException as e:
        logger.warning(f'文件下载失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'文件下载失败 e-{e}')
        raise HTTPException(400, detail=error_info('文件下载失败'))


@router.get('/openFile/{file_id}')
async def open_file(file_id: str):
    """
    转发course网站内openfile指向的文件请求（用于显示图片）
    """
    try:
        session = await User.get_login_session()
        res = session.get(f'https://course2.xmu.edu.cn/meol/common/ckeditor/openfile.jsp?id={file_id}')

        headers = dict(res.headers)
        return Response(content=res.content, headers=headers)
    except CourseHelperException as e:
        logger.warning(f'打开资源失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'打开资源失败 e-{e}')
        raise HTTPException(400, detail=error_info('打开资源失败'))


@router.post('/uploadFile')
async def open_file(data: UploadFileModel):
    try:
        if not os.path.exists(data.file_path):
            raise CourseHelperException('文件不存在')
        session = await User.get_login_session()
        file_name = os.path.basename(data.file_path)
        files = {'file': (file_name, open(data.file_path, 'rb'))}
        file_size = os.path.getsize(data.file_path)

        res = session.post('https://course2.xmu.edu.cn/meol/servlet/SerUpload',
                           files=files)
        if not res.status_code == 200:
            raise CourseHelperException('文件上传失败')

        return success_info('文件上传成功', data={
            'file_url': 'http://127.0.0.1:6498/file/openFile/' + res.text[res.text.find('id=') + 3:],
            'file_name': file_name,
            'file_size': Downloader.byte_to_suitable_size(file_size),
            'file_path': data.file_path
        })
    except CourseHelperException as e:
        logger.warning(f'文件上传失败 - 失败原因:{e}')
        raise HTTPException(400, detail=error_info(e.data))
    except Exception as e:
        logger.debug(f'文件上传失败 e-{e}')
        raise HTTPException(400, detail=error_info('文件上传失败'))
