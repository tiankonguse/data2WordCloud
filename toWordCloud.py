# encoding: utf-8

import json
import re
import time
from http.cookies import SimpleCookie

import jieba.analyse
import matplotlib.pyplot as plt
import requests
from scipy.misc import imread
from wordcloud import WordCloud


def readData(inputFile):
    # 读取数据

    file_obj = open(inputFile)
    all_lines = file_obj.readlines()
    f.close()
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
    generate_img(word_segment(readData()))
