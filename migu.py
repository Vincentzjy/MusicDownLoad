from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import requests
import os
class Migu():
    def __init__(self, key):
        self.key = key
        self.names = []
        self.singers = []
        self.download_urls = []
    def get_urls(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        browser = webdriver.Firefox(firefox_options=options)
        wait = WebDriverWait(browser, 10)
        url = 'https://m.music.migu.cn/v3/search?keyword={}'.format(self.key)
        browser.get(url)
        browser.implicitly_wait(5)
        name = '.left h4'
        singer = 'name_gs'
        music_url = 'play_1'
        def index_music_name(name):
            items = browser.find_elements_by_css_selector(name)
            datas = []
            for item in items:
                datas.append(item.text)
            return datas
        def index_music_singer(singer):
            items = browser.find_elements_by_class_name(singer)
            datas = []
            for item in items:
                datas.append(item.text)
            return datas
        def index_music_url(music_url):
            items = browser.find_elements_by_class_name(music_url)
            datas = []
            for item in items:
                datas.append(item.get_attribute('src'))
            return datas
        self.names = index_music_name(name)
        self.singers = index_music_singer(singer)
        self.download_urls = index_music_url(music_url)
        browser.close()
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
    with open(key + url[-4:], 'wb') as f:
        data = open_url(url)
        f.write(data)