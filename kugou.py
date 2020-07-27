import requests
import os
class Kugou():
    def __init__(self, key):
        self.key = key
        self.names = []
        self.singers = []
        self.albums = []
        self.download_urls = []
    def get_urls(self):
        s = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
            }
        params = {
            'keyword': self.key,
		    'page': '1',
		    'pagesize': '31',
            'userid': '-1',
            'clientver': '',
            'platform': 'WebFilter',
            'tag': 'em',
            'filter': '',
            'iscorrection': '1',
            'privilege_filter': '0'
            }
        url = 'http://songsearch.kugou.com/song_search_v2'
        url2 = 'https://wwwapi.kugou.com/yy/index.php'
        response = s.get(url, headers=headers, params=params)
        items = response.json()['data']['lists']
        for item in items:
            params = {
                'r': 'play/getdata',
		        'hash': str(item['FileHash']),
		        'album_id': str(item['AlbumID']),
		        'dfid': '',
		        'mid': 'ccbb9592c3177be2f3977ff292e0f145',
		        'platid': '4'
                }
            response = s.get(url2, headers=headers, params=params)
            response_json = response.json()
            self.download_urls.append(response_json['data']['play_url'].replace('\\', ''))
            self.names.append(item['SongName'])
            self.singers.append(item['SingerName'])
            self.albums.append(item['AlbumName'])
def open_url(img_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    response = requests.get(img_url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None
def download(key, url, folder):
    os.chdir(folder)
    with open(key + url[-4:], 'wb') as f:
        data = open_url(url)
        f.write(data)  