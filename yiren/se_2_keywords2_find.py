# -*- coding: utf-8 -*-

lines = ''
cnt = 0
keywords = ['双飞','姐妹','群P','群p']
f = open('log_yazhousetu.txt',encoding='UTF-8')
for line in f.readlines():
    boo = 0
    for i in range(len(keywords)):
        boo = boo or (line.find(keywords[i])+1)
    if boo:
        lines = lines + line
        cnt += 1
print(lines)
print('共找到'+str(cnt)+'条结果\n')

file = open("keywords2_find.txt", "w")
file.write('\n共找到'+str(cnt)+'条结果\n\n'+lines)
file.close()
print('log: keywords2_find.txt')
