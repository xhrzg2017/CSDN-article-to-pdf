# CSDN-article-to-pdf
下载CSDN 文章变成pdf文件

调用如下软件完成
wkhtmltopdf https://github.com/wkhtmltopdf/wkhtmltopdf

#代码思路

    网站数据内容来源
        1.确定一下目标要求
            找到文章内容一个来源 确定url地址 文章内容/文章标题
            只需请求 文章url地址 获取它网页源代码 即可获取文章内容以及标题
            怎么找到数据来源
                1.查看导航栏中url返回的数据内容<判断网页类型 静态/动态网页>

#代码实现：

    1.对文章列表 url https://blog.csdn.net/pythonxuexi123/article/list/1 发送请求
    2.获取列表页源代码，提取每篇文章url
    3.对文章url请求
    4.数据解析 提取文章内容/标题
    5.保存数据保存成html
    6.html文件转换成pdf文件
