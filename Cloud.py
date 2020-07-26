from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import requests
import os
class Cloud():
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
        url = 'https://music.163.com/#/search/m/?s={}&type=1'.format(self.key)
        browser.get(url)
        browser.switch_to.frame('contentFrame')
        browser.implicitly_wait(10)
        name = 'w0'
        singer = 'w1'
        album = 'w2'
        music_time = 'td'
        def index_music(infor):
            items = browser.find_elements_by_class_name(infor)
            datas = []
            for item in items:
                datas.append(item.text)
            return datas
        def index_music_url():
            items = browser.find_elements_by_xpath('//div[@class="sn"]//a')
            datas = []
            for item in items:
                datas.append(item.get_attribute('href'))
            return datas
        self.names = index_music(name)
        self.singers = index_music(singer)
        self.albums = index_music(album)
        items = index_music(music_time)
        i = 5
        while i < len(items):
            self.times.append(items[i])
            i += 6
        self.download_urls = index_music_url()
        browser.close()
def download_url(url):
    down = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(url.split('=')[-1])
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
    