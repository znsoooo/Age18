## 功能说明：

- 程序实现从一个图片质量很高的网站上自动下载一些图片。
- 函数包括自动重试下载、建立指定数目线程同步下载、删除空文件、重复运行程序自动跳过已完成的任务、访问网页优先访问本地记录、自动检查用正则表达式匹配到的链接结果是否包含网页内的所有图片。
- 如果网站失效，我不会更新代码，请自行修改。

### 友情提示：

- 如果直接运行可能会抓取到2017-08-04至今的所有资料，超过11.6+GB的内容，163546+张图像。
- GetPage函数用于访问网站指定页码的文章列表。如果不需要下载网站的全部内容，请将页码范围缩小。
- 文章列表会在运行时记录在'urls.txt'文件内。如果需要下载列表里的网址可以运行GetLog(log)函数。

### 函数功能：

- GetLog(file): 下载记录文件中的网址。
- GetPage(page): 下载指定页数的文章列表里的所有文章的所有图片。
- SavePictures(url): 下载指定文章网址中的所有图片。
- DeleteEmptyFile(folder): 删除文件夹内的空文件。


----

## Read me:

- The program will auto download some high quality images from website.
- Functions include auto retry downloading, create threads and download, delete empty files in folder, run program and skip completed tasks, accessing local records if exist, check whether the links matched with regular expression contains all pictures in page.
- If the website is changed, I will not update the code, fix it yourself.

### Hint:

- If run the program directly, it may download data from now to 2017-08-04, that maybe more than 11.6+GB and 163546+ images.
- The "GetPage" function will request exactly page of website and return list of articles. If you do not want download entire website, reduce the scope.
- The list of article urls is recorded in 'urls.txt'. If you want download article from log, you can use "GetLog(log)" function.

### Functions:

- **GetLog(file):** download the list of urls in the log file.
- **GetPage(page):** download images in articles in the list of article page number.
- **SavePictures(url):** download images in the article url.
- **DeleteEmptyFile(folder):** delete empty file in folder.
