import base64
from io import BytesIO
from PIL import Image


def xmu_slider_code(base64_img):
    """
    获取滑块验证码 滑块相对坐标w
    """

    # base64转pil
    img = base64_pil(base64_img[base64_img.find(";base64,") + 8:])
    p = get_img_border(img, True)
    min_len = min([len(t) for t in p if len(t) > 0])
    index = [len(t) for t in p].index(min_len)
    row = p[index]
    return row[int(min_len / 2 if min_len % 2 == 0 else (min_len + 1) / 2)] - 20  # 20为滑块宽度


def base64_pil(base64_str) -> Image.Image:
    """
    base64转pil图片
    """
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = Image.open(image)
    return image


def get_img_border(img, reverse=False) -> list:
    """
    滑块背景图片处理
    """
    x, y = img.size
    pixel_map = img.load()
    out = []
    for i in range(y):
        row = []
        for j in range(x):
            t = pixel_map[(j, i)]
            if reverse:
                if t[3] < 255:  # 说明是半透明点
                    row.append(j)
            else:
                if t[3] > 0:  # 说明是不透明点
                    row.append(j)
        out.append(row)

    return out
