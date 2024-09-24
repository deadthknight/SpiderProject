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

# 字体拆解，保存为单个字体图片，并保存在 imgs 文件夹中

def font_split_single_img(font_path):
    # 解析字体文件
    font = TTFont(font_path)  # woff2文件
    cmap = font.getBestCmap()
    index = 1

    # 创建存放图像的文件夹
    os.makedirs('imgs', exist_ok=True)

    for n, v in cmap.items():
        d = v
        glyph = font.getGlyphSet()[d]  # 通过字形名称选择某一字形对象
        pen = FreeTypePen(None)  # 实例化Pen子类
        glyph.draw(pen)  # “画”出字形轮廓
        b = pen.array()

        # 创建新的图像
        plt.figure(figsize=(2, 2))  # 调整图像大小（这里是2x2英寸）
        plt.imshow(b, cmap='gray_r')  # 设置黑色字形，白色背景
        plt.gca().set_facecolor('white')  # 设置背景为白色
        plt.axis('off')  # 禁用坐标轴

        # 调整边距，防止字形占满整个图像
        plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

        # 保存图片
        plt.savefig(f'./imgs/{d}.jpg', bbox_inches='tight', pad_inches=0.1)  # 设置边框
        plt.close()

        index += 1

    logger.info("图片绘制完成")
    return os.path.join('.', 'imgs')

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
    import time

    starttime = time.time()  # 获取开始时间
    img_dir= font_split_single_img(font_path='./font/96fc7b50b772f52.woff2')
    imagesPath= ocrWords(img_dir)
    word_map = readImagName('imgs_copy_word')
    endtime = time.time()
    # print(word_map)
    elapsed_time = endtime - starttime  # 计算时间差
    logger.info(elapsed_time)