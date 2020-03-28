# -*- coding:utf-8 -*-
#!/usr/bin/python

# 20180131
# 解决了抓包timeout超时会导致程序中断的问题
# 20180211
# 解决了读取的网页文本和写入文件格式不一致的问题
# 程序代码中的域名参数化
# 404错误时跳过编号

import urllib
import urllib.request
import urllib.error
# import urllib2
import socket  
import re
import time

url1 = 'http://www.yiren07.com'
url2 = '/se/yazhousetu/'

print('Author Lsx Start:')
print(time.strftime("%Y-%m-%d %H:%M:%S"))

text = '\n' + 'Start time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n' + '\n'
text = text + url1 + url2 + '\n' + '\n'
file = open("log.txt", "w")
file.write(text)
file.close()
text = ''

i = 1
while(i < 1970):
    if i == 1:
        url = (url1 + url2)
    else:
        url = (url1 + url2 + 'index_' + str(i) + '.html')
    print('Page ' + str(i))

    #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}  
    try:
        # request = urllib2.Request(url, headers = headers)
        # response = urllib2.urlopen(request, timeout = 2) # 2秒超时
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request, timeout = 2) # 2秒超时
        
        content = response.read().decode('utf-8')
        # print(content)
        text = text + '\n' + 'Page ' + str(i) + '\n' + '\n'

        pattern = re.compile('<ul class="textList">(.*?)</ul>',re.S)
        content = re.findall(pattern,content)

        pattern = re.compile('<li><a href="' + url2 + '(.*?)" target="_blank" title="(.*?)"><span>(.*?)</span>',re.S)
        items = re.findall(pattern,content[0])
        for item in items:
            # print item[0]
            text = text + item[0] + '\t' + item[2] + '\t' + item[1] + '\n'

    # except urllib2.URLError, e:
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
            print(2)
        if hasattr(e,"reason"):
            print(e.reason)
        if e.code == 404:
            i = i + 1 # 抵消掉i自减重试
        i = i - 1
    except socket.timeout as e:  
        print(type(e))
        i = i - 1

    i = i + 1
    
    file = open("log.txt", "a", encoding = 'utf-8') # encoding = 'utf-8' 解决 'gbk' codec can't encode character 问题
    file.write(text)
    file.close()
    text = ''

text = '\n' + 'Finish time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n' + '\n'
file = open("log.txt", "a")
file.write(text)
file.close()

print('Author Lsx End:')
print(time.strftime("%Y-%m-%d %H:%M:%S"))
