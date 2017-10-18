#-*- coding:utf8 -*-
import json
from lxml import etree, html
import os
import requests

url = "http://www.ximalaya.com/10936615/album/7651313/" #喜马拉雅《晓说》专辑页面
dst_folder = u'晓说'

#url = "http://www.ximalaya.com/81960855/album/8273989/" #喜马拉雅《细读张爱玲》专辑页面
#dst_folder = u'细读张爱玲'

raw_cookies = "BAIDUID=C443462CF12F13BC2D3C168B0193230B:FG=1; BIDUPSID=C443462CF12F13BC2D3C168B0193230B; PSTM=1507545083; PSINO=7; H_PS_PSSID=1466_21080_22157; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; FP_UID=af9b57b6627c7c99a89ad48ce3d911f2"
def build_cookies():
	cookies = {}
	for line in raw_cookies.split(';'):
		key, value = line.split('=', 1)
		key, value = key.strip('\r\n\t '), value.strip('\r\n\t ')
		cookies[key] = value
	return cookies

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}

if __name__ == "__main__":
	cookies = build_cookies()
	res = requests.get(url,headers = headers, cookies = cookies)
	html = etree.HTML(res.text)

	#print(type(res.content)) 	# bytes
	#print(type(res.text))		# str

	#1. 每个 音频ID 的 显示音频名字
	m4a_id_title = {}
	#m4a_list = html.xpath("//div[@class='album_soundlist ']/ul/li")	#喜马拉雅前端开发在album_soundlist后面多写了一个空格，所以我用正则来匹配更易于今后容错
	m4a_list = html.xpath("//div[contains(@class, 'album_soundlist')]/ul/li")
	for m4a_desc in m4a_list:
		m4a_id = m4a_desc.attrib['sound_id']
		m4a_title = m4a_desc.xpath(".//a[@class='title']")[0].text.strip('\r\n\t ')
		if m4a_id and m4a_title:
			m4a_id_title[m4a_id] = m4a_title

	#2. 本专辑音频ID列表
	try:
		os.mkdir(dst_folder)
	except Exception as e:
		print(e)

	for m4a_id in m4a_id_title.keys():
		m4a_title = m4a_id_title[m4a_id]
		if not m4a_title:
			m4a_title = m4a_id

		try:
			# 拿到音频url
			m4a_url = 'http://www.ximalaya.com/tracks/{}.json'.format(m4a_id)
			m4a_info_str = requests.get(m4a_url,headers=headers).text
			m4a_info_json = json.loads(m4a_info_str)
			m4a_url = m4a_info_json['play_path']	#目前喜马拉雅付费节目只支持移动端播放
			#print('%s downloading...'%(m4a_url))

			# 下载音频
			res = requests.get(m4a_url, headers = headers, cookies = cookies) # stream=True
			if res and res.status_code == requests.codes.ok:
				with open('%s/%s.m4a'%(dst_folder, m4a_title), 'wb') as f:
					#f.write(res.content)
					for chunk in res.iter_content(chunk_size=1024):
						if chunk:
							f.write(chunk)
							#f.flush() #commented by recommendation from J.F.Sebastian
					print('%s downloaded'%(m4a_title))
		except Exception as e:
			print('%s download failed'%(m4a_title))
			print(e)