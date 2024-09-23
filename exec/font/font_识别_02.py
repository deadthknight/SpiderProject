# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import io
import os
import re

import ddddocr
from PIL import ImageDraw, ImageFont, Image
from fontTools.ttLib import TTFont


class UniversalFontRecognition(object):
    ocr = None

    def __init__(self, font_path):
        self.font_path = font_path
        self.ocr = ddddocr.DdddOcr(show_ad=False)

    def font_to_xml(self, xml_path=None):
        if not xml_path:
            # 不指定路径，则默认在当前目录下转换
            filename_with_ext = os.path.basename(self.font_path)
            filename_only = os.path.splitext(filename_with_ext)[0]
            xml_path = f'{filename_only}.xml'
        font = TTFont(self.font_path)
        font.saveXML(xml_path)

    def font_to_img(self, char_list, img_size=100, font_ratio=0.7):
        normal_dict = {}

        for char in char_list:
            char_code = chr(char).encode().decode()
            img = Image.new('RGB', (img_size, img_size), 255)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(self.font_path, int(img_size * font_ratio))
            x, y = draw.textsize(char_code, font=font)
            draw.text(((img_size - x) // 2, (img_size - y) // 2), char_code, font=font, fill=0)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            image_bytes = img_bytes.getvalue()
            word = self.ocr.classification(image_bytes)
            normal_dict[char] = word[0] if word else ''

        return normal_dict

    def crack(self):
        """ 最终转成的都是unicode的映射 {unicode：识别结果}, 调用时需要将文本转成unicode """
        with open(self.font_path, 'rb') as fr:
            font_bytes = fr.read()
        with TTFont(io.BytesIO(font_bytes)) as font_parse:  # 码点与字体编码对应
            u_d = font_parse.getBestCmap()  # 返回字体中可用的“最佳”unicode cmap字典
        return self.font_to_img(list(u_d.keys()))
