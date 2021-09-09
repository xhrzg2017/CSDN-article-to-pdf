#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @编辑器        : PyCharm 
# @项目名        : csdn
# @文件名        : demo.py
# @作者          : xhrzg2017 
# @邮箱          : xhrzg2017@gmail.com
# @团队          : 广州电脑初哥工作室
# @创建时间       : 2021/4/24 11:01 
# @Editor       : PyCharm 
# @Project_Name : csdn
# @File_Name    : demo.py
# @Author       : xhrzg2017 
# @Email        : xhrzg2017@gmail.com
# @Team         : Guangzhou computer novice studio
# @Time         : 2021/4/24 11:01


html_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title></title>
</head>    
<body> 
{article} 
</body>
</html>
"""


def change_title(title):
    '''替换标题特殊字符变成‘_’'''
    mode = re.compile(r'[\/\\\:\*\?\"\<\>\|]')
    new_title = re.sub(mode, '_', title)
    return new_title


'''
网站数据内容来源
    1.确定一下目标要求
        找到文章内容一个来源 确定url地址 文章内容/文章标题
        只需请求 文章url地址 获取它网页源代码 即可获取文章内容以及标题
        怎么找到数据来源
            1.查看导航栏中url返回的数据内容<判断网页类型 静态/动态网页>

    代码实现：
        1.对文章列表 url https://blog.csdn.net/pythonxuexi123/article/list/1 发送请求
        2.获取列表页源代码，提取每篇文章url
        3.对文章url请求
        4.数据解析 提取文章内容/标题
        5.保存数据保存成html
        6.html文件转换成pdf文件
'''

import requests
import parsel
import re
import pdfkit
import os
import time


def get_page(user):
    url = f'https://blog.csdn.net/{user}/article/list/1'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
    }
    response = requests.get(url=url, headers=headers)
    selector_page = parsel.Selector(response.text)
    page1 = selector_page.css('#container-header-blog').get()
    # print(page1)
    page2 = re.findall(r'\d+', page1)
    page3 = int(page2[0])
    if page3 % 40 > 0:
        page = page3 // 40 + 1
    else:
        page = page3 // 40
    # print(page)
    return page


def csdn(user):
    page = get_page(user)
    for page in range(1, int(page + 1)):
        time.sleep(0.2)
        # 对文章列表发送请求
        url = f'https://blog.csdn.net/{user}/article/list/{page}'
        print('=' * 20 + f'正在爬取第{page}页' + '=' * 20)
        # headers 请求头
        # 为什么加 把py代码伪装成浏览器请求
        # 加什么 UA:浏览器信息，host:域名, cookie:用户信息, referer：防盗链
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
        }
        response = requests.get(url=url, headers=headers)
        # print(response.text)

        # 获取列表页源代码，提取每篇文章url
        # 把网页文本数据转换成selector对象
        selector = parsel.Selector(response.text)
        # css选择器
        # getall()取多个标签 get()取单个 attr取属性名字 text 取标签文本数据
        href = selector.css('.article-list div.article-item-box h4 a::attr(href)').getall()
        # 正则表达式 <a href="(.*?)" target="_blank"
        # print(href)
        for link in href:
            time.sleep(1)
            # 对文章url请求
            html_data = requests.get(url=link, headers=headers).text
            # 数据解析 提取文章内容/标题
            # id='xxx' css('#xxx') class='aaa' css(.aaa')
            selector_l = parsel.Selector(html_data)
            title = selector_l.css('#articleContentId::text').get()
            new_title = change_title(title)
            content = selector_l.css('#content_views').get()
            html = html_str.format(article=content)
            html_filename = 'pdf\\' + new_title + '.html'
            pdf_filename = 'pdf\\' + new_title + '.pdf'
            # 保存数据保存成html
            with open(html_filename, mode='w', encoding='utf-8')as f:
                f.write(html)
                print('正在保存', title)
            # 导入软件 html文件转换成pdf文件
            config = pdfkit.configuration(wkhtmltopdf=r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
            pdfkit.from_file(html_filename, pdf_filename, configuration=config)
            os.remove(html_filename)


if __name__ == '__main__':
    user = input('请输入下载的博客用户名：')
    csdn(user)
