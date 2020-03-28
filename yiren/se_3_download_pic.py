# -*- coding:utf-8 -*-
#!/usr/bin/python

import urllib
import urllib.request
import urllib.error
# import urllib2
import socket  
import re
import time

url1 = 'http://www.yiren07.com'
url2 = '/se/yazhousetu/'

in_path  = 'keywords2_find.txt'
out_path = 'download_pic.txt'

print('Author Lsx Start:')
print(time.strftime("%Y-%m-%d %H:%M:%S"))

text = '\n' + 'Start time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n' + '\n'
file = open(out_path, "w")
file.write(text)
file.close()
text = ''

f1 = open(in_path)
f2 = f1.read().split('\n')
f3 = []
for i in range(len(f2)):
    f3.append(f2[i].split('\t'))

i = 1
while(i < len(f3)):
    if(f3[i][0].find('html') + 1):
        url = (url1 + url2 + f3[i][0])
        # url = 'http://www.yiren07.com/se/yazhousetu/592583.html'
        print(url)
        text = text + url + '\n'

        #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}  
        try:
            request = urllib.request.Request(url, headers = headers)
            response = urllib.request.urlopen(request, timeout = 2) # 2秒超时
            
            content = response.read().decode('utf-8')
            # print(content)
            pattern = re.compile('<div class="novelContent">(.*?)</div>',re.S)
            content = re.findall(pattern,content)

            pattern = re.compile('<img.*?src="(.*?)"',re.S)
            items = re.findall(pattern,content[0])
            for item in items:
                # print(item)
                text = text + item + '\n'

        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print(e.code)
                if e.code == 404: # 放到外面会可能出现 'URLError' object has no attribute 'code'
                    i = i + 1 # 抵消掉i自减重试
            if hasattr(e,"reason"):
                print(e.reason)
            i = i - 1
        except socket.timeout as e:  
            print(type(e))
            i = i - 1

    i = i + 1

    file = open(out_path, "a", encoding = 'utf-8') # encoding = 'utf-8' 解决 'gbk' codec can't encode character 问题
    file.write(text)
    file.close()
    text = ''
    
text = '\n' + 'Finish time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n' + '\n'
file = open(out_path, "a")
file.write(text)
file.close()

print('Author Lsx End:')
print(time.strftime("%Y-%m-%d %H:%M:%S"))
