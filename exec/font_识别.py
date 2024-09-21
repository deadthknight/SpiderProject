from fontTools.ttLib import TTFont
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
import ddddocr  # 确保已安装并导入 ddddocr


def read_num_by_draw(woff_font):
    """
    绘制图片通过ddddocr库进行图片识别
    :param woff_font: 字体文件
    :return: 字体字典
    """
    img_size = 512
    font = TTFont(woff_font)  # 这里传递字体文件路径
    font_img = ImageFont.truetype(woff_font, img_size)  # 使用 woff 字体文件
    ocr = ddddocr.DdddOcr(show_ad=False)
    font_dict = {}

    for cmap_code, glyph_name in font.getBestCmap().items():
        # 实例化一个图片对象
        img = Image.new('1', (img_size, img_size), 255)

        # 绘制图片
        draw = ImageDraw.Draw(img)
        txt = chr(cmap_code)  # 将编码读取成字符

        # 获取文本的边界框
        bbox = draw.textbbox((0, 0), txt, font=font_img)
        x = bbox[2] - bbox[0]  # 宽度
        y = bbox[3] - bbox[1]  # 高度

        draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font_img, fill=0)

        bytes_io = BytesIO()
        img.save(bytes_io, format="PNG")

        # 识别字体
        word = ocr.classification(bytes_io.getvalue())
        font_dict[glyph_name.replace('uni', '&#x').lower()] = word

    return font_dict
