import os
from loguru import logger
from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
from PIL import Image
import ddddocr
import json

# 设置 matplotlib 后端为 'Agg'，用于在无 GUI 环境下生成图像
matplotlib.use('Agg')


# 日志配置
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置全局路径变量，增强代码的可移植性


# 字体拆解，保存为单个字体图片，并保存在 imgs 文件夹中
def font_split_single_img(font_path):
    # 解析字体文件
    font = TTFont(font_path)  # woff2文件
    cmap = font.getBestCmap()
    # font.saveXML('font.xml')  # 保存存为xml
    index = 1
    for n, v in cmap.items():
        d = v
        glyph = font.getGlyphSet()[d]  # 通过字形名称选择某一字形对象
        pen = FreeTypePen(None)  # 实例化Pen子类
        glyph.draw(pen)  # “画”出字形轮廓
        # pen.show()    # 显示
        b = pen.array()
        # print(index, '/', len(cmap), '~~~', glyph)
        plt.figure()
        plt.imshow(b)
        plt.axis('off')  # 禁用坐标轴
        os.makedirs('imgs', exist_ok=True)
        plt.savefig('./imgs/{0}.jpg'.format(d))
        # # plt.show()    # 显示
        # plt.clf()
        # plt.cla()
        plt.close()
        index += 1

    logger.info("图片绘制完成")
    logger.info()
    return os.path.join('.','imgs')


# 使用 ddddocr 识别拆解后的字体图片，并保存到 imgs_copy_word 文件夹
def ocrWords(img_dir):
    ocr = ddddocr.DdddOcr(beta=False, show_ad=False)  # 实例化 ddddocr 识别器
    img_copy_dir = os.path.join('.', 'imgs_copy_word')
    word_map = {}

    os.makedirs(img_copy_dir, exist_ok=True)  # 确保 imgs_copy_word 目录存在

    # 遍历 imgs 文件夹中的所有图片
    for parent, dirnames, filenames in os.walk(img_dir):
        for filename in filenames:
            k = filename.split('.')[0]  # 提取文件名（不带扩展名）
            currentPath = os.path.join(parent, filename)

            try:
                # 打开图片文件并识别文字
                img = Image.open(currentPath)
                image_bytes = BytesIO()
                img.save(image_bytes, format='JPEG')
                res = ocr.classification(image_bytes.getvalue())

                # 如果未能识别或识别结果为空
                if len(res) == 0:
                    res = '未找到'
                if len(res) > 1:
                    res = res[0]  # 只取第一个字符

                # 保存识别结果为新文件，命名为 {原文件名}__{识别结果}.jpg
                new_filename = f'{k}__{res}.jpg'
                img.save(os.path.join(img_copy_dir, new_filename))

                word_map[k] = res
                # logger.info(f"Processed {filename} -> {new_filename}")
            except Exception as e:
                logger.error(f"Error processing {filename}: {e}")

    logger.info('图片识别完毕')
    return os.path.join('.','img_copy_dir')


# 读取识别后的图片名称，并将结果存储为字典，返回映射关系

# 根据识别后的名称，提取结果，并保存为 .json文件：dddddocr识别的保存为：ocr_dddd.json
def readImagName(imagesPath, saveJsonName='ocr_dddd.json'):
    word_map = {}
    for parent, dirnames, filenames in os.walk(imagesPath):  # 遍历每一张图片
        for filename in filenames:
            k = filename.split('.')[0]
            res = k.split('__')[1]
            word_map[k.split('__')[0]] = res
    if word_map:
        with open(saveJsonName, 'w', encoding='utf-8') as f:
            f.write(json.dumps(word_map, ensure_ascii=False))
    logger.info('字典已生成')
    return word_map


if __name__ == "__main__":
    # 分解字体并生成图片
    font_split_single_img(font_path='./font/96fc7b50b772f52.woff2')
