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
        self.download_urls = []
    def get_urls(self):
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=62949948419074461&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={}&g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'.format(self.key)
        headers = {
            'referer': 'https://y.qq.com/portal/search.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        s = requests.Session()
        response = s.get(url, headers=headers)
        items = response.json()['data']['song']['list']
        for item in items:
            t = ''
            self.names.append(item['name'])
            for i in item['singer']:
                t += i['name']
                t = t + '/'
            self.singers.append(t)
            self.albums.append(item['album']['name'])
            self.download_urls.append('https://y.qq.com/n/yqq/song/' + item['mid'] + '.html')
def download_url(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=options) 
    except:
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