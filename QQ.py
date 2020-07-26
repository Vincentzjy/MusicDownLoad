from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
import os
class QQ_music():
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
        url = 'https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w={}'.format(self.key)
        browser.get(url)
        browser.implicitly_wait(5)
        name = 'js_song'
        singer = 'singer_name'
        album = 'album_name'
        song_time = 'songlist__time'
        music_url = 'js_song'
        def index_music(infor):
            items = browser.find_elements_by_class_name(infor)
            datas = []
            for item in items:
                datas.append(item.text)
            return datas
        def index_music_url(infor):
            items = browser.find_elements_by_class_name(infor)
            datas = []
            for item in items:
                datas.append(item.get_attribute('href'))
            return datas
        self.names = index_music(name)
        self.singers = index_music(singer)
        self.albums = index_music(album)
        self.times = index_music(song_time)
        self.download_urls = index_music_url(music_url)
        browser.close()
def download_url(url):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(firefox_options=options)
    wait = WebDriverWait(browser, 10)
    browser.get('http://www.douqq.com/qqmusic/')
    browser.implicitly_wait(5)
    input = browser.find_element_by_id('mid')
    input.send_keys(url)
    button = browser.find_element_by_id('sub')
    button.click()
    time.sleep(5)
    down = browser.find_element_by_id('m4a').text
    browser.close()
    return down
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
    result = download_url(url)
    with open(key + result.split('?')[0][-4:], 'wb') as f:
        data = open_url(result)
        f.write(data)