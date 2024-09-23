from fontTools.ttLib import TTFont
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
import ddddocr  # OCR库

def read_num_by_draw(woff_font):
    img_size = 1024  # 适中的图片大小，确保字符清晰
    font = TTFont(woff_font)  # 读取字体文件
    font_img = ImageFont.truetype(woff_font, img_size)  # 创建字体对象
    ocr = ddddocr.DdddOcr(show_ad=False)  # 实例化OCR对象
    font_dict = {}  # 用于存储识别结果

    for cmap_code, glyph_name in font.getBestCmap().items():
        # 创建白色背景的图像
        img = Image.new('L', (img_size, img_size), 255)
        draw = ImageDraw.Draw(img)  # 创建绘图对象
        txt = chr(cmap_code)  # 将 cmap_code 转换为对应的字符

        # 获取文本的边界框
        bbox = draw.textbbox((0, 0), txt, font=font_img)
        x = bbox[2] - bbox[0]  # 计算文本宽度
        y = bbox[3] - bbox[1]  # 计算文本高度

        # 将文本绘制在图片中心
        draw.text(((img_size - x) // 2, (img_size - y) // 7), txt, font=font_img, fill=0)

        bytes_io = BytesIO()  # 创建内存中的字节流
        img.save(bytes_io, format="PNG")  # 将图片保存到字节流中

        # 使用OCR识别文本
        img_bytes = bytes_io.getvalue()  # 获取图像的字节数据
        word = ocr.classification(img_bytes)  # 使用ddddocr进行识别
        glyph_key = f"&#x{glyph_name[3:].lower()};" if glyph_name.startswith('uni') else glyph_name.lower()

        # 将识别结果存入字典
        font_dict[glyph_key] = word

    return font_dict  # 返回识别结果的字典
# def font_to_img(_code, font_path):
#     '''
#     将每个字体画成图片
#     :param _code:字体的数字码点
#     :param font_path:字体文件路径
#     :return:每个字体图片对象
#     '''
#
#     img_size =1024
#     img =Image.new('1',(img_size,img_size),255)
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype(font_path,int(img_size * 0.7))
#     txt = chr(_code)
#     bbox = draw.textbbox((0,0),txt,font=font)
#     x= bbox[2] - bbox[0]
#     y= bbox[3]- bbox[1]
#     draw.text(((img_size-x)//2,(img_size-y)//7),txt,font=font,fill=0)
#     return img

