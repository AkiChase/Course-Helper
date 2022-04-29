import time


def success_info(msg: str, success: int = 1, **kwargs) -> dict:
    out = {
        'msg': msg,
        'success': success
    }
    out.update(kwargs)
    return out


def error_info(msg: str, success: int = 0, **kwargs) -> dict:
    out = {
        'msg': msg,
        'success': success
    }
    out.update(kwargs)
    return out


class CourseHelperException(Exception):
    """
    自定义异常
    """
    data: dict

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data
