# encoding: utf-8

import json
import re
import time

import matplotlib.pyplot as plt
import jieba.analyse
from scipy.misc import imread
#import imageio
from wordcloud import WordCloud


def readData(inputFile):
    # 读取数据

    file_obj = open(inputFile)
    all_lines = file_obj.readlines()
    file_obj.close()
    return all_lines


def word_segment(texts):
    # 分词处理
    jieba.analyse.set_stop_words("./stopwords.txt")
    text = " ".join(texts)
    tags = jieba.analyse.extract_tags(text, topK=100)
    return tags


def generate_img(texts):
    # 生成词云图片
    data = " ".join(text for text in texts)

    mask_img = imread('./tiankonguse-logo.jpg', flatten=True)
    wordcloud = WordCloud(
        background_color='white',
        mask=mask_img
    ).generate(data)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('./wordcloud.jpg', dpi=600)


if __name__ == '__main__':
    generate_img(word_segment(readData("data.txt")))
