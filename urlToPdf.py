# encoding: utf-8

from __future__ import unicode_literals
import json
import re
import time
import logging
import os
import re
import time
import matplotlib.pyplot as plt
import jieba.analyse
from scipy.misc import imread
#import imageio
from wordcloud import WordCloud
from urllib.parse import urlparse
import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>

"""
html_template_null = """
{content}

"""
headers = {
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Cookie': 'rewardsn='
}

def readData(url):
    """
    网络请求,返回response对象
    :return:
    """
    response = requests.get(url,headers=headers)
    return response

def parse_body(response, domain):
    """
    解析正文
    :param response: 爬虫返回的response对象
    :return: 返回处理后的html文本
    """
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find_all(id="page-content")[0]
        #body = soup

        # 加入标题, 居中显示
        #title = soup.find('h2').get_text()
        #center_tag = soup.new_tag("center")
        #title_tag = soup.new_tag('h1')
        #title_tag.string = title
        #center_tag.insert(1, title_tag)
        #body.insert(1, center_tag)

        html = str(body)
        # body中的img标签的src相对路径的改成绝对路径
        pattern = "(<img .*?src=\")(.*?)(\")"

        def func(m):
            m2=m.group(2)
            if not m2.startswith("http"):
                print (m2)
                rtn = "".join([m.group(1), domain, m2, m.group(3)])
                return rtn
            else:
                #m2=m2.split("?")
                #m2=m2[0]+"?tp=jpeg"
                m2 = m2.replace("https", "http")
                print (m2)
                return "".join([m.group(1), m2, m.group(3)])
        html = re.compile(pattern).sub(func, html)
        #html = html_template_null.format(content=html)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
        #html = str(html)
        #print (html)
        return html
    except Exception as e:
        logging.error("解析错误", exc_info=True)
        return ""

def run(url):
    start = time.time()
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    htmls = []
    html = parse_body(readData(url), domain)
    index = 0
    f_name = ".".join([str(index), "html"])
    with open(f_name, 'wb') as f:
        f.write(html)
    htmls.append(f_name)
    pdfkit.from_file(htmls, "test.pdf", options=options)
    #for html in htmls:
    #    os.remove(html)
    total_time = time.time() - start
    print(u"总共耗时：%f 秒" % total_time)
    


if __name__ == '__main__':
    run("https://mp.weixin.qq.com/s/CFFuSqWpbyzMDuT5FrBmcw")
