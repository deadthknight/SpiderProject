from fontTools.ttLib import TTFont
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
import ddddocr  # OCR库


def read_num_by_draw(woff_font):
    img_size = 512  # 图片大小
    font = TTFont(woff_font)  # 读取字体文件
    font_img = ImageFont.truetype(woff_font, img_size)  # 创建字体对象
    ocr = ddddocr.DdddOcr(show_ad=False)  # 实例化OCR对象
    font_dict = {}  # 用于存储识别结果

    for cmap_code, glyph_name in font.getBestCmap().items():
        img = Image.new('1', (img_size, img_size), 255)  # 创建白色背景的图片
        draw = ImageDraw.Draw(img)  # 创建可以绘制的对象
        txt = chr(cmap_code)  # 将 cmap_code 转换为对应的字符

        # 获取文本的边界框
        bbox = draw.textbbox((0, 0), txt, font=font_img)
        x = bbox[2] - bbox[0]  # 计算文本宽度
        y = bbox[3] - bbox[1]  # 计算文本高度

        # 将文本绘制在图片中心
        draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font_img, fill=0)

        bytes_io = BytesIO()  # 创建一个内存中的字节流
        img.save(bytes_io, format="PNG")  # 将图片保存到字节流中

        # 使用OCR识别文本
        word = ocr.classification(bytes_io.getvalue())
        font_dict[glyph_name.replace('uni', '&#x').lower()] = word  # 将识别结果存入字典

    return font_dict  # 返回识别结果的字典
