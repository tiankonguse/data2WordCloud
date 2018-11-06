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
import sys

style_css="""
           .radius_avatar {
                display: inline-block;
                background-color: #fff;
                padding: 3px;
                border-radius: 50%;
                -moz-border-radius: 50%;
                -webkit-border-radius: 50%;
                overflow: hidden;
                vertical-align: middle
            }

            .radius_avatar img {
                display: block;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                -moz-border-radius: 50%;
                -webkit-border-radius: 50%;
                background-color: #eee
            }

            .rich_media_inner {
                word-wrap: break-word;
                -webkit-hyphens: auto;
                -ms-hyphens: auto;
                hyphens: auto
            }

            .rich_media_area_primary {
                padding: 20px 16px 12px;
                background-color: #fafafa
            }

            .rich_media_area_primary.voice {
                padding-top: 66px
            }

            .rich_media_area_primary .weui-loadmore_line .weui-loadmore__tips {
                color: rgba(0,0,0,0.3);
                background-color: #fafafa
            }

            .rich_media_area_extra {
                padding: 0 16px 24px
            }

            .rich_media_extra {
                padding-top: 30px
            }

            .mpda_bottom_container .rich_media_extra {
                padding-top: 24px
            }

            html {
                -ms-text-size-adjust: 100%;
                -webkit-text-size-adjust: 100%;
                line-height: 1.6
            }

            body {
                -webkit-touch-callout: none;
                font-family: -apple-system-font,BlinkMacSystemFont,"Helvetica Neue","PingFang SC","Hiragino Sans GB","Microsoft YaHei UI","Microsoft YaHei",Arial,sans-serif;
                color: #333;
                letter-spacing: .034em
            }

            * {
                margin: 0;
                padding: 0
            }

            a {
                color: #576b95;
                text-decoration: none;
                -webkit-tap-highlight-color: rgba(0,0,0,0)
            }

            .rich_media_title {
                font-size: 22px;
                line-height: 1.4;
                margin-bottom: 14px
            }

            @supports(-webkit-overflow-scrolling:touch) {
                .rich_media_title {
                    font-weight: 700
                }
            }

            .rich_media_meta_list {
                margin-bottom: 22px;
                line-height: 20px;
                font-size: 0;
                word-wrap: break-word;
                word-break: break-all
            }

            .rich_media_meta_list em {
                font-style: normal
            }

            .rich_media_meta {
                display: inline-block;
                vertical-align: middle;
                margin: 0 10px 10px 0;
                font-size: 15px;
                -webkit-tap-highlight-color: rgba(0,0,0,0)
            }

            .rich_media_meta.icon_appmsg_tag {
                margin-right: 4px
            }

            .rich_media_meta.meta_tag_text {
                margin-right: 0
            }

            .rich_media_meta_primary {
                display: block;
                margin-bottom: 10px;
                font-size: 15px
            }

            .meta_original_tag {
                padding: 0 .5em;
                font-size: 12px;
                line-height: 1.4;
                background-color: #f2f2f2;
                color: #888
            }

            .meta_enterprise_tag img {
                width: 30px;
                height: 30px!important;
                display: block;
                position: relative;
                margin-top: -3px;
                border: 0
            }

            .rich_media_meta_link {
                color: #576b95
            }

            .rich_media_meta_text {
                color: rgba(0,0,0,0.3)
            }

            .rich_media_meta_text.rich_media_meta_split {
                padding-left: 10px
            }

            .rich_media_meta_text.rich_media_meta_split:before {
                position: absolute;
                top: 50%;
                left: 0;
                margin-top: -6px;
                content: ' ';
                display: block;
                border-left: 1px solid #888;
                width: 200%;
                height: 130%;
                box-sizing: border-box;
                -moz-box-sizing: border-box;
                -webkit-box-sizing: border-box;
                -webkit-transform: scale(0.5);
                transform: scale(0.5);
                -webkit-transform-origin: 0 0;
                transform-origin: 0 0
            }

            .rich_media_meta_text.article_modify_tag {
                position: relative
            }

            .rich_media_meta_nickname {
                position: relative
            }

            .rich_media_thumb_wrp {
                margin-bottom: 6px
            }

            .rich_media_thumb_wrp .original_img_wrp {
                display: block
            }

            .rich_media_thumb {
                display: block;
                width: 100%
            }

            .rich_media_content {
                overflow: hidden;
                color: #333;
                font-size: 17px;
                word-wrap: break-word;
                -webkit-hyphens: auto;
                -ms-hyphens: auto;
                hyphens: auto;
                text-align: justify
            }

            .rich_media_content * {
                max-width: 100%!important;
                box-sizing: border-box!important;
                -webkit-box-sizing: border-box!important;
                word-wrap: break-word!important
            }

            .rich_media_content p {
                clear: both;
                min-height: 1em
            }

            .rich_media_content em {
                font-style: italic
            }

            .rich_media_content fieldset {
                min-width: 0
            }

            .rich_media_content .list-paddingleft-2 {
                padding-left: 2.2em
            }

            .rich_media_content .list-paddingleft-2 .list-paddingleft-2 {
                padding-left: 30px
            }

            .rich_media_content blockquote {
                margin: 0;
                padding-left: 10px;
                border-left: 3px solid #dbdbdb
            }

            .weui-mask {
                position: fixed;
                z-index: 1000;
                top: 0;
                right: 0;
                left: 0;
                bottom: 0;
                background: rgba(0,0,0,0.6)
            }
"""

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
<style>
    {style_css}
</style>
</head>
<body>
{content}
</body>
</html>

"""

def parse_html(htmlText):
    try:
        
        result = re.search(r'var publish_time = "([^"]*)"', htmlText)
        print ("publish_time", result)
        publish_time = ""
        if result:
            publish_time = result.group(1)
            
            
        result = re.search(r'var nickname = "([^"]*)"', htmlText)
        print ("nickname", result)
        nickname  = ""
        if result:
            nickname  = result.group(1)
            
            
        result = re.search(r'var msg_title = "([^"]*)"', htmlText)
        print ("msg_title", result)
        msg_title   = ""
        if result:
            msg_title   = result.group(1)
            
        result = re.search(r'var msg_desc = "([^"]*)"', htmlText)
        print ("msg_desc", result)
        msg_desc   = ""
        if result:
            msg_desc   = result.group(1)
            
        result = re.search(r'var msg_cdn_url = "([^"]*)"', htmlText)
        print ("msg_cdn_url", result)
        msg_cdn_url  = ""
        if result:
            msg_cdn_url   = result.group(1)
        
        soup = BeautifulSoup(htmlText, 'html.parser')
        body = soup.find_all(class_="rich_media_content ")[0]
        #body = soup

        #body = soup.find_all("body")[0]
        # 加入标题, 居中显示
        center_tag = soup.new_tag("center")
        title_tag = soup.new_tag('h2')
        title_tag.string = msg_title
        center_tag.insert(1, title_tag)
        body.insert(1, center_tag)
        
        #加入作者 和 日期
        div_tag = soup.new_tag("div")
        div_tag['class'] = 'rich_media_meta_list'
        nickname_tag = soup.new_tag('span')
        nickname_tag.string = nickname
        nickname_tag['class'] = 'rich_media_meta rich_media_meta_text'
        div_tag.insert(1, nickname_tag)
        
        publish_time_tag = soup.new_tag('span')
        publish_time_tag.string = publish_time
        publish_time_tag['class'] = 'rich_media_meta rich_media_meta_text'
        div_tag.insert(1, publish_time_tag)
        
        body.insert(2, div_tag)
        
        #加入简介
        blockquote_tag = soup.new_tag("blockquote")
        if len(msg_desc) != 0:
            msg_desc_tag = soup.new_tag('span')
            msg_desc_tag.string = msg_desc
            blockquote_tag.insert(1, msg_desc_tag)
        blockquote_tag["style"] = "padding: 20px 8px;line-height: 2em; background-color: #f2f2f2; margin-bottom: 20px";
        body.insert(3, blockquote_tag)
            
        
        #加入题图
        div_tag = soup.new_tag("div")
        if len(msg_cdn_url) != 0:
            msg_cdn_url_tag = soup.new_tag("img")
            msg_cdn_url_tag["src"] = msg_cdn_url
            div_tag.insert(1, msg_cdn_url_tag)
        body.insert(4, div_tag)
        
        
        img_tags = body.find_all('img')
        for img_obj in img_tags:
            attrs = img_obj.attrs 
            if "src" not in attrs and "data-src" in attrs:
                attrs["src"] = attrs["data-src"]
        
        html = str(body)

        html = html_template.format(content=html, style_css=style_css)
        #html = html.encode("utf-8")
        return html
    except Exception as e:
        print("解析错误")
        print(e.what())
        return ""

def run(htmlFile, pdfFile):
    start = time.time()
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
    
    print("begin read %s" % (htmlFile))
    with open(htmlFile, 'r') as f:
        htmlText = f.read()
    htmlText = parse_html(htmlText)
    
    print("begin write tmp.html")
    with open("./tmp.html", 'w') as f:
        f.write(str(htmlText))
    
    htmls.append("tmp.html")
    ret = pdfkit.from_file(htmls, pdfFile, options=options)
    total_time = time.time() - start
    print(u"ret[%d] 总共耗时：%f 秒" % (ret,total_time))
    

def usage():
    print ("%s htmlFile pdfFile"% (sys.argv[0]))
    
if __name__ == '__main__':
    argc = len(sys.argv)
    print ("argc[%d]"% (argc))
    if argc != 3:
        usage()
    else:
        htmlFile = sys.argv[1]
        pdfFile = sys.argv[2]
        run(htmlFile, pdfFile)
