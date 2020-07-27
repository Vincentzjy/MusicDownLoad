import requests
import os
class Kuwo():
    def __init__(self, key):
        self.key = key
        self.names = []
        self.singers = []
        self.albums = []
        self.times = []
        self.download_urls = []
    def get_urls(self):
        url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn=1&rn=30&httpsStatus=1&reqId=69ef2300-cc93-11ea-8cc7-59bea742bef0'.format(self.key)
        headers = {
            'Cookie': 'kw_token=VDFN9QJHGCO',
            'csrf': 'VDFN9QJHGCO',
            'Referer': 'http://www.kuwo.cn/search/list?key=%E5%9A%A3%E5%BC%A0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
            }
        response = requests.get(url, headers=headers).json()
        results = response['data']['list']
        for result in results:
            self.download_urls.append(result['rid'])
            self.names.append(result['name'])
            self.singers.append(result['artist'])
            self.albums.append(result['album'])
            self.times.append(result['songTimeMinutes'])
def download_url(url):
    get_url = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1595473768850&httpsStatus=1&reqId=ebe99721-cc91-11ea-8cc7-59bea742bef0'.format(url)
    headers = {
        'Cookie': 'kw_token=VDFN9QJHGCO',
        'csrf': 'VDFN9QJHGCO',
        'Referer': 'http://www.kuwo.cn/search/list?key=%E5%9A%A3%E5%BC%A0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
    }
    response = requests.get(get_url, headers=headers).json()
    data = response['url']
    return data
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
    with open(key + result[-4:], 'wb') as f:
        data = open_url(result)
        f.write(data)  