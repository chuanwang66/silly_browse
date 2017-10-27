# silly_browse
The right way in which a programmer surfs the Internet !


* a crawler built by Selenium & openpyxl	呼出浏览器
```
# C:\Python35\Scripts\pip.exe install selenium
# C:\Python35\Scripts\pip.exe install openpyxl
# C:\Python35\python.exe super_fish.py
```

* a crawler built by grequests & lxml	自动获取cookie，不呼出浏览器，支持并发抓取 (但不支持非阻塞IO)
```
# C:\Python35\Scripts\pip.exe install requests
# C:\Python35\Scripts\pip.exe install grequests
# C:\Python35\Scripts\pip.exe install lxml
# C:\Python35\Scripts\pip.exe install openpyxl
# C:\Python35\python.exe super_fish2.py
```

* super_fish2_session.py 把super_fish2.py改造成session方式实现

* super_fish3.py 尝试用 "线程池+requests"方式 实现 非阻塞网络IO
  在开发中，我们往往更需要的是这种 "非阻塞IO"，而不是 "并发IO"(除非你在做爬虫)

* 下载喜马拉雅(非付费)音频
```
# C:\Python35\python.exe super_fish_ximalaya.py
```
![](https://raw.githubusercontent.com/chuanwang66/silly_browse/master/resources/super_fish_ximalaya.jpg)