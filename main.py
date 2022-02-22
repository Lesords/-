from PyQt5.QtCore import QBasicTimer, Qt

from window import *
from spider import *
from dialog import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from multiprocessing import Process, Pool
import time
import datetime
import sys


class ButtonFunc(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ButtonFunc, self).__init__(parent)
        self.setupUi(self)
        spider = Spider()
        self.up_quick.clicked.connect(lambda: spider.new_crawl(0))  # lambda可以重写默认信号参数
        self.new_song.clicked.connect(lambda: spider.new_crawl(1))
        self.original.clicked.connect(lambda: spider.new_crawl(2))
        self.hot_song.clicked.connect(lambda: spider.new_crawl(3))
        self.all_list.clicked.connect(lambda: spider.crawl_all())


class Spider():
    def __init__(self):
        self.url = "https://music.163.com/discover/toplist?id="
        self.id = ['19723756', '3779629', '2884035', '3778678'] # 飙升榜、新歌榜、原创榜、热歌榜
        self.name = ['飙升榜', '新歌榜', '原创榜', '热歌榜']

    def new_crawl(self, list_id):
        work = Process(target=self.find_list, args=(list_id, 1))
        work.start()    # 无需等待，自己会结束

    def crawl_all(self):
        work = Process(target=self.find_all)
        work.start()

    def find_list(self, list_id, flag):
        print("正在爬取%sing" % self.name[list_id])
        begin = time.time()
        today = datetime.datetime.now()
        today = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
        file_name = self.name[list_id] + ' ' + today + ".xls"
        crawl(self.url+self.id[list_id], file_name)
        end = time.time()
        print("爬取结束，花费时间为%.3f秒" % (end-begin))
        if flag:
            show_dialog()

    def find_all(self):
        print("开始爬取")
        begin = time.time()
        p = Pool(4)
        for i in range(4):
            # 花费时间为15.543s
            # work = Process(target=self.new_crawl, args=(i,))
            # work.start()
            # work.join()

            # 花费的总时间为7.420秒
            # p.apply(self.find_list, args=(i,))        # 堵塞方法无需join

            p.apply_async(self.find_list, args=(i, 0))    # 需要join才会运行完整个进程池的程序

        p.close()
        p.join()                                        # 等待进程池程序运行完
        end = time.time()
        print("所有数据已爬取成功，所花费的总时间为%.3f秒" % (end-begin))
        show_dialog()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    user_interface = ButtonFunc(main_window)
    user_interface.show()
    sys.exit(app.exec_())