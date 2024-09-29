# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
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
from multiprocessing.dummy import Pool  # 导入多线程池

# 设置 matplotlib 后端为 'Agg'
matplotlib.use('Agg')

def process_single_glyph(glyph_name, glyph):
    try:
        pen = FreeTypePen(None)
        glyph.draw(pen)  # “画”出字形轮廓
        b = pen.array()

        # 创建新的图像
        plt.figure(figsize=(2, 2))
        plt.imshow(b, cmap='gray_r')
        plt.gca().set_facecolor('white')
        plt.axis('off')
        plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

        # 保存图片
        os.makedirs('imgs', exist_ok=True)
        plt.savefig(f'./imgs/{glyph_name}.jpg', bbox_inches='tight', pad_inches=0.1)
        plt.close()

        return f"{glyph_name} processed successfully"
    except Exception as e:
        return f"Error processing {glyph_name}: {str(e)}"

def font_split_single_img(font_path):
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()

    # 创建线程池
    with Pool() as pool:
        results = pool.starmap(process_single_glyph, [(glyph_name, glyph_set[glyph_index]) for glyph_name, glyph_index in cmap.items()])

    # 输出处理结果
    for result in results:
        logger.info(result)

    logger.info("图片绘制完成")
    return os.path.join('.', 'imgs')

def process_single_image(img_path, ocr):
    try:
        img = Image.open(img_path)
        image_bytes = BytesIO()
        img.save(image_bytes, format='JPEG')
        res = ocr.classification(image_bytes.getvalue())

        if len(res) == 0:
            res = '未找到'
        elif len(res) > 1:
            res = res[0]

        return os.path.basename(img_path), res
    except Exception as e:
        logger.error(f"Error processing {img_path}: {e}")
        return os.path.basename(img_path), None

def ocrWords(img_dir):
    ocr = ddddocr.DdddOcr(beta=False, show_ad=False)
    img_copy_dir = os.path.join('.', 'imgs_copy_word')
    os.makedirs(img_copy_dir, exist_ok=True)

    # 创建线程池
    with Pool() as pool:
        results = pool.map(lambda img: process_single_image(os.path.join(img_dir, img), ocr), os.listdir(img_dir))

    word_map = {}
    for filename, res in results:
        if res:
            new_filename = f'{filename.split(".")[0]}__{res}.jpg'
            img = Image.open(os.path.join(img_dir, filename))
            img.save(os.path.join(img_copy_dir, new_filename))
            word_map[filename.split('.')[0]] = res

    logger.info('图片识别完毕')
    return img_copy_dir

def readImagName(imagesPath, saveJsonName='ocr_dddd.json'):
    word_map = {}
    for parent, dirnames, filenames in os.walk(imagesPath):
        for filename in filenames:
            k = filename.split('.')[0]
            res = k.split('__')[1]
            word_map[k.split('__')[0]] = res
    if word_map:
        with open(saveJsonName, 'w', encoding='utf-8') as f:
            json.dump(word_map, f, ensure_ascii=False)
    logger.info('字典已生成')
    return word_map

if __name__ == "__main__":
    import time

    starttime = time.time()  # 获取开始时间
    img_dir = font_split_single_img(font_path='./font/96fc7b50b772f52.woff2')
    imagesPath = ocrWords(img_dir)
    word_map = readImagName('./imgs_copy_word')
    endtime = time.time()  # 获取结束时间

    elapsed_time = endtime - starttime  # 计算时间差
    logger.info(elapsed_time) # 打印耗时

