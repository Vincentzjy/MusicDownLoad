from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
import time
import os
import QQ
import Cloud
import qianqian
import kuwo
import kugou
import migu
names = []
download_urls = []
exts = []
def index():
    infor = combo.get()
    key = entry1.get()
    if infor in ['QQ', '网易云', '千千', '酷我', '酷狗', '咪咕']:
        if key != '':
            global download_urls
            global names
            global exts
            text.delete(0, END)
            text.insert(END, '正在搜索......')
            text.see(END)
            text.update()
            if infor == 'QQ':
                music = QQ.QQ_music(key)
                music.get_urls()
                text.delete(0, END)
                for i in range(len(music.names) - 1):
                    text.insert(END, str(i + 1) + '/' + music.names[i] + '/' + music.singers[i] + '/' + music.albums[i] + '/' + music.times[i])
                download_urls = music.download_urls
                names = music.names
            elif infor == '网易云':
                music = Cloud.Cloud(key)
                music.get_urls()
                text.delete(0, END)
                for i in range(len(music.names) - 1):
                    text.insert(END, str(i + 1) + '/' + music.names[i] + '/' + music.singers[i] + '/' + music.albums[i] + '/' + music.times[i])
                download_urls = music.download_urls
                names = music.names
            elif infor == '千千':
                music = qianqian.Qian(key)
                music.get_urls()
                text.delete(0, END)
                for i in range(len(music.names) - 1):
                    text.insert(END, str(i + 1) + '/' + music.names[i] + '/' + music.singers[i] + '/' + music.albums[i])
                download_urls = music.download_urls
                names = music.names
            elif infor == '酷我':
                music = kuwo.Kuwo(key)
                music.get_urls()
                text.delete(0, END)
                for i in range(len(music.names) - 1):
                    text.insert(END, str(i + 1) + '/' + music.names[i] + '/' + music.singers[i] + '/' + music.albums[i] + '/' + music.times[i])
                download_urls = music.download_urls
                names = music.names
            elif infor == '酷狗':
                music = kugou.Kugou(key)
                music.get_urls()
                text.delete(0, END)
                for i in range(len(music.names) - 1):
                    text.insert(END, str(i + 1) + '/' + music.names[i] + '/' + music.singers[i] + '/' + music.albums[i])
                download_urls = music.download_urls
                names = music.names
            elif infor == '咪咕':
                music = migu.Migu(key)
                music.get_urls()
                text.delete(0, END)
                for i in range(len(music.names) - 1):
                    text.insert(END, str(i + 1) + '/' + music.names[i] + '/' + music.singers[i] + '/' + music.albums[i])
                download_urls = music.download_urls
                names = music.names
                exts = music.exts
def down_load():
    infor = combo.get()
    if infor in ['QQ', '网易云', '千千', '酷我', '酷狗', '咪咕']:
        key = entry1.get()
        number = entry2.get()
        if int(number) > 0 and int(number) < len(names):
            text.delete(0, END)
            folder = tkinter.filedialog.askdirectory()
            text.insert(END, '正在下载......')
            text.see(END)
            text.update()
            if infor == 'QQ':
                try:
                    QQ.download(names[int(number) - 1], download_urls[int(number) - 1], folder)
                    text.delete(0, END)
                    text.insert(END,'下载成功')
                except:
                    text.delete(0, END)
                    text.insert(END,'下载失败')
            elif infor == '网易云':
                try:
                    Cloud.download(names[int(number) - 1], download_urls[int(number) - 1], folder)
                    text.delete(0, END)
                    text.insert(END,'下载成功')
                except:
                    text.delete(0, END)
                    text.insert(END,'下载失败')
            elif infor == '千千':
                try:
                    qianqian.download(names[int(number) - 1], download_urls[int(number) - 1].split('/')[-1], folder)
                    text.delete(0, END)
                    text.insert(END,'下载成功')
                except:
                    text.delete(0, END)
                    text.insert(END,'下载失败')
            elif infor == '酷我':
                try:
                    kuwo.download(names[int(number) - 1], download_urls[int(number) - 1], folder)
                    text.delete(0, END)
                    text.insert(END,'下载成功')
                except:
                    text.delete(0, END)
                    text.insert(END,'下载失败')
            elif infor == '酷狗':
                try:
                    kugou.download(names[int(number) - 1], download_urls[int(number) - 1], folder)
                    text.delete(0, END)
                    text.insert(END,'下载成功')
                except:
                    text.delete(0, END)
                    text.insert(END,'下载失败')
            elif infor == '咪咕':
                try:
                    migu.download(names[int(number) - 1], download_urls[int(number) - 1], folder, exts[int(number) - 1])
                    text.delete(0, END)
                    text.insert(END,'下载成功')
                except:
                    text.delete(0, END)
                    text.insert(END,'下载失败')
root = Tk()
root.title('音乐下载器')
root.geometry('400x700')
label1 = Label(root, text='请输入歌曲源')
label1.grid()
combo = Combobox(root)
combo['values'] = ('QQ', '网易云', '千千', '酷我', '酷狗', '咪咕')
combo.current(0)
combo.grid(row=0, column=1)
label2 = Label(root, text='请输入歌曲关键词')
label2.grid(row=1, column=0)
entry1 = Entry(root)
entry1.grid(row=1, column=1)
button2 = Button(root, text='搜索', command=index)
button2.grid(row=1, column=2)
text = Listbox(root, width=50, heigh=30)
text.grid(row=3, columnspan=3)
label3 = Label(root, text='请输入歌曲序号')
label3.grid(row=4, column=0, sticky=W)
entry2 = Entry(root)
entry2.grid(row=4, column=1)
button1 = Button(root, text='下载歌曲', command=down_load)
button1.grid(row=4, column=2, sticky=E)
root.mainloop()