#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time
import sys

timeout = 5
# 代表经过t秒后，如果还未下载成功，自动跳入下一次操作，此次下载失败。
socket.setdefaulttimeout(timeout)


class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0    #结尾数量
    __start_amount = 0   #开始个数
    __counter = 0  #文件名的第几个
    __category = 100  #种类类别，用于保运在图片名称上
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 判断图像类别
    def get_category(self, word):
        all_category = ['苍术中药', '苍耳子中药', '决明子中药', '枳实中药', '天花粉中药', '黄连中药']
        return all_category.index(word)

    # 获取后缀名
    def get_suffix(self, name):
        # \.是匹配.的意思 ^\.是匹配不是.的字符 [^\.]是匹配任意不是.的字符当中的一个   [^\.]*匹配0个或任意多个不是.的字符  匹配到$结束符    search方法扫描整个字符串并返回第一个成功的匹配
        m = re.search(r'\.[^\.]*$', name)
        # print("m为：" + str(m))
        # group(0)就是指匹配的完整字符串  group(1)是指串中串
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取referrer，用于生成referrer
    def get_referrer(self, url):
        # 将url分成六个部分，返回一个包含6个字符串项目的元组：协议，位置，路径，参数，查询，判断。scheme是协议  例如scheme='https'  scheme是位置  例如netloc='mbd.baidu.com'
        par = urllib.parse.urlparse(url)
        if par.scheme:
            return par.scheme + '://' + par.netloc
        else:
            return par.netloc

        # 保存图片
    def save_image(self, rsp_data, word):
        if not os.path.exists(self.__saveDirectoryPath + "/" + word):
            os.mkdir(self.__saveDirectoryPath + "/" + word)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir(self.__saveDirectoryPath + "/" + word)) + 1
        for image_info in rsp_data['imgs']:
            # print("image_info为：" + str(image_info))
            try:
                time.sleep(self.time_sleep)
                suffix = self.get_suffix(image_info['objURL'])
                # 指定UA和referrer，减少403
                refer = self.get_referrer(image_info['objURL'])
                # 方便修改报头
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'),
                    ('Referer', refer)
                ]
                # 使用定义的opener作为全局opener
                urllib.request.install_opener(opener)
                # 保存图片  urlretrieve()方法直接将远程数据下载到本地   param1:下载地址  param2：本地保存位置
                urllib.request.urlretrieve(image_info['objURL'], self.__saveDirectoryPath + '/' + word + '/' + str(self.__category) + '-' + str(self.__counter) + str(suffix))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            # 当没有异常发生时，执行else语句
            else:
                print("中药饮片图片+1,已有" + str(self.__counter) + "张图片")
                self.__counter += 1
        return

    # 开始获取
    def get_images(self, word='中药'):
        # 大概意思是，按照标准，URL只允许一部分ASCII字符，其他字符（如汉字）是不符合标准的，此时就要进行编码。因为我在构造URL的过程中要使用到中文：
        search = urllib.parse.quote(word)
        # pn int 图片数
        pn = self.__start_amount
        while pn < self.__amount:

            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # print("一页的url信息: " + url)
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                # 返回一个response对象, 返回信息保存在此对象里.
                page = urllib.request.urlopen(req)
                # read方法, 可以返回获取到的网页内容
                rsp = page.read().decode('unicode_escape')
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                # 解析json
                rsp_data = json.loads(rsp)
                self.save_image(rsp_data, word)
                # 读取下一页
                print("下载下一页")
                pn += 60
            finally:
                page.close()
        print("下载任务结束")
        return

    def start(self, word, start_page=1, spider_page_num=1, DirectoryPath='.'):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param spider_page_num: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param start_page:起始页数
        :return:
        """
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.__category = self.get_category(word)
        self.__saveDirectoryPath = DirectoryPath
        self.get_images(word)


if __name__ == '__main__':

    # crawler.start('苍术中药', 1, 10)  # 抓取关键词，总数为 10 页（即总共 10*60=600 张），开始页码为 1   从第6页开始，爬取五页       1,10    11,10
    # crawler.start('苍耳子中药', 1, 10)
    # crawler.start('决明子中药', 1, 10)
    # crawler.start('枳实中药', 1, 10)
    # crawler.start('天花粉中药', 1, 10)
    # crawler.start('黄连中药', 1, 10)
    if len(sys.argv) != 5:
        print("输入格式错误")
    else:
        crawler = Crawler(1)  # 抓取延迟为 0.05
        crawler.start(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])