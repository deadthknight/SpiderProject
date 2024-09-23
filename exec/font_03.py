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
    # font_path = os.path.join(FONT_DIR, '96fc7b50b772f52.woff2')  # 读取字体文件路径
    IMG_DIR = os.path.join('.', 'imgs')
    try:
        # 解析字体文件
        font = TTFont(font_path)
    except FileNotFoundError:
        logger.error(f"Font file {font_path} not found.")
        return

    cmap = font.getBestCmap()  # 获取字体映射表
    os.makedirs(IMG_DIR, exist_ok=True)  # 确保 imgs 目录存在

    index = 1
    pen = FreeTypePen(None)  # 实例化 Pen 类，避免重复创建
    for n, v in cmap.items():
        glyph = font.getGlyphSet()[v]  # 获取字形对象
        glyph.draw(pen)  # 绘制字形轮廓
        b = pen.array()  # 获取字形轮廓的图像数组

        # 使用 matplotlib 保存字形为图片
        plt.figure()
        plt.imshow(b)
        plt.axis('off')  # 隐藏坐标轴
        plt.savefig(os.path.join(IMG_DIR, f'{v}.jpg'))  # 保存图片到 imgs 文件夹
        plt.close()

        # logger.info(f"Processed glyph {index}/{len(cmap)}: {v}")
        index += 1

    logger.info("图片绘制完成")
    return IMG_DIR

# 使用 ddddocr 识别拆解后的字体图片，并保存到 imgs_copy_word 文件夹
def ocrWords(IMG_DIR):
    ocr = ddddocr.DdddOcr(beta=False, show_ad=False)  # 实例化 ddddocr 识别器
    IMG_COPY_DIR = os.path.join('.', 'imgs_copy_word')
    word_map = {}

    os.makedirs(IMG_COPY_DIR, exist_ok=True)  # 确保 imgs_copy_word 目录存在

    # 遍历 imgs 文件夹中的所有图片
    for parent, dirnames, filenames in os.walk(IMG_DIR):
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
                img.save(os.path.join(IMG_COPY_DIR, new_filename))

                word_map[k] = res
                # logger.info(f"Processed {filename} -> {new_filename}")
            except Exception as e:
                logger.error(f"Error processing {filename}: {e}")

    logger.info('图片识别完毕')
    return IMG_COPY_DIR

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
    # font_split_single_img()
    IMG_DIR= font_split_single_img('./font/96fc7b50b772f52.woff2')
    IMG_COPY_DIR= ocrWords(IMG_DIR)
    # 识别图片中文字
    word_map = readImagName(IMG_COPY_DIR)

    # 输出识别结果
    print(word_map)