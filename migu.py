import requests
import os
class Migu():
    def __init__(self, key):
        self.key = key
        self.names = []
        self.singers = []
        self.download_urls = []
        self.exts = []
    def get_urls(self):
        search_url = 'http://pd.musicapp.migu.cn/MIGUM3.0/v1.0/content/search_all.do'
        player_url = 'https://app.pd.nf.migu.cn/MIGUM3.0/v1.0/content/sub/listenSong.do?channel=mx&copyrightId={copyrightId}&contentId={contentId}&toneFlag={toneFlag}&resourceType={resourceType}&userId=15548614588710179085069&netType=00'
        params = {
					'ua': 'Android_migu',
					'version': '5.0.1',
					'text': self.key,
					'pageNo': '1',
					'pageSize': '30',
					'searchSwitch': '{"song":1,"album":0,"singer":0,"tagSong":0,"mvSong":0,"songlist":0,"bestShow":1}',
				}
        headers = {
            'Referer': 'https://m.music.migu.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
            }
        s = requests.Session()
        response = s.get(search_url, headers=headers, params=params)
        items = response.json()['songResultData']['result']
        for item in items:
            for rate in sorted(item.get('rateFormats', []), key=lambda x: int(x['size']), reverse=True):
                ext = '.flac' if rate.get('formatType') == 'SQ' else '.mp3'
                self.exts.append(ext)
                self.download_urls.append(player_url.format(copyrightId=item['copyrightId'], contentId=item['contentId'], toneFlag=rate['formatType'], resourceType=rate['resourceType']))
                break
            self.names.append(item['name'])
            for i in item['singers']:
                self.singers.append(i['name'])
def open_url(img_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
    }
    response = requests.get(img_url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None
def download(key, url, folder, ext):
    os.chdir(folder)
    with open(key + ext, 'wb') as f:
        data = open_url(url)
        f.write(data)