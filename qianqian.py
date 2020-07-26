from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import requests
import os
class Qian():
    def __init__(self, key):
        self.key = key
        self.names = []
        self.singers = []
        self.albums = []
        self.download_urls = []
    def get_urls(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        browser = webdriver.Firefox(firefox_options=options)
        wait = WebDriverWait(browser, 10)
        url = 'http://music.taihe.com/'
        browser.get(url)
        browser.implicitly_wait(5)
        input_key = browser.find_element_by_xpath('//*[@id="kw"]')
        input_key.send_keys(self.key)
        input_key.send_keys(Keys.ENTER)
        browser.switch_to_window(browser.window_handles[1])
        time.sleep(5)
        name = 'song-title'
        singer = 'author_list'
        album = 'album-title'
        def index_music(infor):
            items = browser.find_elements_by_class_name(infor)
            datas = []
            for item in items:
                datas.append(item.text)
            return datas
        def index_music_url():
            items = browser.find_elements_by_xpath('//span[@class="song-title"]/a')
            datas = []
            for item in items:
                datas.append(item.get_attribute('href'))
            return datas
        self.names = index_music(name)
        self.singers = index_music(singer)
        self.albums = index_music(album)
        self.download_urls = index_music_url()
        browser.close()
def download_url(id):
    url = 'http://play.taihe.com/data/music/songlink'
    data = {
        'songIds': id,
        'hq': '0',
        'type': 'm4a,mp3',
        'rate': '',
        'pt': '0',
        'flag': '-1',
        's2p': '-1',
        'prerate': '-1',
        'bwt': '-1',
        'dur': '-1',
        'bat': '-1',
        'bp': '-1',
        'pos': '-1',
        'auto': '-1'
    }
    response = requests.post(url,data=data)
    results = response.json()['data']['songList']
    for result in results:
        music_url = result['songLink']
    return music_url
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
    with open(key + result.split('?')[0][-4:], 'wb') as f:
        data = open_url(result)
        f.write(data) 