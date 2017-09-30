#-*- coding:utf8 -*-
"""
	C:\Python35\Scripts\pip.exe install requests
	#C:\Python35\Scripts\pip.exe install beautifulsoup4
	C:\Python35\Scripts\pip.exe install lxml
"""
#from bs4 import BeautifulSoup
import io
import lxml
import requests
import sys

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def check_connection(url):
    try:
        request = requests.head(url)
        if request.status_code == 200:
            print('Connection ok...')
            return True
        elif request.status_code == 301:
            print('Connection redirect')
            return True
        else:
            print('Error connecting')
            return False
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print('{} can not be reached, check your connection and retry later'.format(url))
        return False
    except (requests.exceptions.HTTPError, requests.exceptions.TooManyRedirects):
        print('There is an issue with the url, {}, confirm it, or retry later'.format(url))
        return False

def download(url, local_filename):
	res = requests.get(url, stream=True)
	if res and res.status_code == requests.codes.ok:
		#total_size = int(res.headers['content-length'])
		#download_size = 0
		with open(local_filename, 'wb') as f:
			for chunk in res.iter_content(chunk_size=1024):
				if chunk:  # filter out keep-alive new chunks
					f.write(chunk)
					#f.flush() #commented by recommendation from J.F.Sebastian

					#download_size += len(chunk)
		return True
	else:
		return False

headers_ximalaya = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def test_ximalaya():
	res = requests.get('http://www.ximalaya.com/dq/all{}'.format(1), headers=headers1)

	#save in local file
	#with open('local.html', 'wb') as f:
	#	f.write(res.text.encode(res.encoding))

	#print in cmd
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
	#print(res.text)

	#lxml可以用xpath语法，我比较习惯一些:)
	html = lxml.etree.HTML(res.text)
	albums = html.xpath("//div[@class='albumfaceOutter']")
	for album in albums:
		print(album.xpath("./a/span/img")[0].get('alt'))

	"""
	#soup = BeautifulSoup(res.text, 'lxml')
	soup = BeautifulSoup(res.text, 'html5lib')
	for item in soup.find_all(class_="albumfaceOutter"):
		content = {
			'href': item.a['href'],
			'title': item.img['alt'],
			'img_url': item.img['src']
		}
		print(content)
	"""

if __name__ == "__main__":
	#download('https://github.com/chuanwang66/silly_player_x/archive/master.zip', 'silly_player_x.zip')
	test_ximalaya()
	