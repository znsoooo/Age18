# built  : 20200326
# github : github.com/znsoooo/Age18/tree/master/javxxx

import os
import re
import time
import urllib.request
from threading import Thread


log = 'urls.txt'
illegal = '\t\/:*?"<>|'
th_cnt = 0


def pprint(s):
    print(s + '\n', end='')


def AddThread(th_max=10):
    global th_cnt
    while th_cnt > th_max:
        pass
    th_cnt += 1
    return th_cnt


def PopThread():
    global th_cnt
    th_cnt -= 1
    return th_cnt


def DeleteEmptyFile(folder, minisize=0):
    cnt = 0
    for path, folders, files in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            if os.path.getsize(filename) <= minisize:
                os.remove(filename)
                cnt += 1
    pprint('DeleteEmptyFile: %s'%cnt)
    return cnt


def GetUrlData(url, retry=10):
    for i in range(retry): # retry
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request, timeout=10)
            content = response.read()
            if len(content): # zero and continue
                return content
        except:
            pass
    return b'' # retry fail and return as default


def GetArticle(url):
    id = url.split('/')[-2]
    os.makedirs('image/%s'%id, exist_ok=1)
    html = 'image/%s/article.html'%id
    if os.path.exists(html) and os.path.getsize(html):
        with open(html, encoding='u8') as f:
            article = f.read()
    else:
        content = GetUrlData(url).decode()
        article = (re.findall(r'(<article[\s\S]*?</article>)', content) + [''])[0] # never return empty (request fail or findall fail)
        with open(html, 'w', encoding='u8') as f:
            f.write(article)
    return article


def SavePictures(url):
    id = url.split('/')[-2]

    # check exist html file or request from web
    article = GetArticle(url)
    if not article:
        PopThread()
        return []

    # check exist image file
    exists = [file for file in os.listdir('image\%s'%id) if file[-4:] not in ['.txt','html']]

    cover  = re.findall(r'<div class="image-container">[\s\S]*?data-src="(.*?)"', article) # cover always one (or 0)
    if len(cover) == 0:
        cover = ['']
        # pprint('No cover: %s'%url)
    imgs   = re.findall(r'<img.*?src="([^"]*?)" *>', article)
    imgs   = [url.replace('\n','') for url in imgs] # Hint: several urls contain '\n' in line.
    pictures = cover + imgs

    srcs   = re.findall(r'src="([\s\S]*?)"', article)
    srcs2  = [src for src in srcs if src[-4:] in ['.jpg','.png']]
    srcs2  = [url.replace('\n','') for url in srcs2] # Hint: several urls contain '\n' in line.

    # exist files == max images in html == find images by re
    if len(exists) == len(srcs2) == (len(pictures) - (cover[0] == '')):
        # pprint('Perfect: %s'%id)
        PopThread()
        return pictures

    # reserved for check download completely but not write images
##    pprint('%s %s %s %s'%(len(exists), len(srcs2), (len(pictures)-(cover[0]=='')), id)) #  + '\n'.join(pictures)
##    PopThread()
##    return

    title = re.findall(r'<h1 class="post-title entry-title">(.*?)</h1>', article)[0]

    if len(pictures) < 5:
        pprint('%sP: %s %s'%(len(pictures), id, title[:30] + ' ...'))

    with open('image/%s/%s.txt'%(id, id), 'w', encoding='u8') as f:
        f.write('\n'.join([title] + pictures))

    for cnt, img_url in enumerate(pictures):
        if img_url == '':
            continue
        root, ext = os.path.splitext(img_url)
        content = GetUrlData(img_url)
        with open('image/%s/%02d%s'%(id, cnt, ext), 'wb') as f:
            f.write(content)

    PopThread()
    return pictures


def GetPage(page):
    url = 'https://javxxx.club/page/%s/'%page
    content = GetUrlData(url).decode()
    passages = re.findall(  r'<time class="published updated" datetime="(.*?)">'
                          + r'[\s\S]*?'
                          + r'<a href="(.*?)" rel="bookmark"', content)
    pprint('GetPage %s: %s'%(page, len(passages)))

    with open(log, 'a') as f:
        f.write('')
    with open(log) as f:
        urls = f.read().split('\n')
    for date, url in passages:
        if date + ' ' + url in urls:
            pass
        else:
            pprint('GetUrlNew: %s'%url)
            with open(log, 'a') as f:
                f.write(date + ' ' + url + '\n')

        AddThread()
        Thread(target=SavePictures, args=(url,)).start()

    return passages


def GetLog(file):
    with open(log) as f:
        urls = f.read().split('\n')
    for cnt, url in enumerate(urls):
        if url:
            url = url.split()[-1]
            AddThread(20)
            Thread(target=SavePictures, args=(url,)).start()




##GetLog(log)

##passages = GetPage(2)

##DeleteEmptyFile('image')


# Maybe 10GB+ datas will be downloaded
# If no need so much images, reduce the scope.
for i in range(0, 650):
    passages = GetPage(i+1)


##SavePictures('https://javxxx.club/rki-479/')
##SavePictures('https://javxxx.club/iene852/')
