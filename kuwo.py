from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
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
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        browser = webdriver.Firefox(firefox_options=options)
        wait = WebDriverWait(browser, 10)
        url = 'http://www.kuwo.cn/search/list?key={}'.format(self.key)
        browser.get(url)
        browser.implicitly_wait(5)
        name = 'song_name'
        singer = 'song_artist'
        album = 'song_album'
        song_time = 'song_time'
        def index_music(infor):
            items = browser.find_elements_by_class_name(infor)
            datas = []
            for item in items:
                datas.append(item.text)
            return datas
        def index_music_url(key):
            url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn=1&rn=30&httpsStatus=1&reqId=69ef2300-cc93-11ea-8cc7-59bea742bef0'.format(key)
            headers = {
                'Cookie': 'kw_token=VDFN9QJHGCO',
                'csrf': 'VDFN9QJHGCO',
                'Referer': 'http://www.kuwo.cn/search/list?key=%E5%9A%A3%E5%BC%A0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
                }
            response = requests.get(url, headers=headers).json()
            results = response['data']['list']
            rids = []
            for result in results:
                rids.append(result['rid'])
            return rids
        self.names = index_music(name)
        self.singers = index_music(singer)
        self.albums = index_music(album)
        self.times = index_music(song_time)
        self.download_urls = index_music_url(self.key)
        browser.close()
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