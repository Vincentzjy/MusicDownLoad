import requests
import json
import os
from Crypto.Cipher import AES
import base64
import codecs
class Cracker():
	def __init__(self):
		self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
		self.nonce = '0CoJUm6Qyw8W8jud'
		self.pubKey = '010001'
	def get(self, text):
		text = json.dumps(text)
		secKey = self._createSecretKey(16)
		encText = self._aesEncrypt(self._aesEncrypt(text, self.nonce), secKey)
		encSecKey = self._rsaEncrypt(secKey, self.pubKey, self.modulus)
		post_data = {
					'params': encText,
					'encSecKey': encSecKey
					}
		return post_data
	def _aesEncrypt(self, text, secKey):
		pad = 16 - len(text) % 16
		if isinstance(text, bytes):
			text = text.decode('utf-8')
		text = text + str(pad * chr(pad))
		secKey = secKey.encode('utf-8')
		encryptor = AES.new(secKey, 2, b'0102030405060708')
		text = text.encode('utf-8')
		ciphertext = encryptor.encrypt(text)
		ciphertext = base64.b64encode(ciphertext)
		return ciphertext
	def _rsaEncrypt(self, text, pubKey, modulus):
		text = text[::-1]
		rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
		return format(rs, 'x').zfill(256)
	def _createSecretKey(self, size):
		return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]
class Cloud():
    def __init__(self, key):
        self.key = key
        self.names = []
        self.singers = []
        self.albums = []
        self.download_urls = []
    def get_urls(self):
        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        params = {
            's': self.key,
            'type': '1',
            'offset': '0',
            'sub': 'false',
            'limit': '31'
            }
        headers = {
            'referer': 'https://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        s = requests.Session()
        cracker = Cracker()
        response = s.post(url, headers=headers, params=params, data=cracker.get(params))
        items = response.json()['result']['songs']
        for item in items:
            self.names.append(item['name'])
            t = ''
            for i in item['ar']:
                t += i['name']
                t = t + '/'
            self.singers.append(t)
            self.albums.append(item['al']['name'])
            self.download_urls.append(item['privilege']['id'])
        
def download_url(url):
    down = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(url)
    return down
def open_url(img_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
    }
    response = requests.get(img_url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None
def download(key, url, folder):
    os.chdir(folder)
    result = download_url(url)
    with open(key + result.split('/')[-1][-4:], 'wb') as f:
        data = open_url(result)
        f.write(data)
    