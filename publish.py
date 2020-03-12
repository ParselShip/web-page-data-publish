# -*- coding: UTF-8 -*-
import os
import re

import pymysql
import random
from shenjianshou import upload
from setting import *
import time
import concurrent.futures
from seo import seo_api


class Claim:
    def __init__(self):
        self.conn = pymysql.connect(host='128.14.85.130', port=3306, user='zhanqundata', password='PRn733wAGX3M2Eic',
                                    db='zhanqundata', charset='utf8')
        self.cursor = self.conn.cursor()

    def get_num(self):
        """返回统计数量 类型：字典"""
        try:
            self.cursor.execute(" select count(*) from novel ;")
            number = self.cursor.fetchone()
        except Exception as e:
            print('>>> get_name query keyword number Error:', e)
        else:
            return number[0]

    def get_title(self, title_number):
        title = []
        try:
            id = random.randint(1, title_number)
            self.cursor.execute(" select title from novel where id={id} ;".format(id=id))
            results = self.cursor.fetchone()
        except Exception as e:
            print('>>> get_title query mysql Error:', e)
        else:
            for i in range(random.randint(4, 6)):
                title.append(results[0])
            return title

    def get_content(self, title_number):
        title = []
        for i in self.get_title(self.get_num())[1:]:
            title.append('<p>' + i + '</p>')
        try:
            id = random.randint(1, title_number)
            self.cursor.execute(" select content from novel where id={id} ;".format(id=id))
            results = self.cursor.fetchone()
            results = seo_api(results[0]).split('。')
        except Exception as e:
            print('>>> get_content query mysql Error:', e)
        else:
            results.extend(title)
            results.insert(0, get_pic())
            random.shuffle(results)
            return ''.join(results), title[0].strip('<p></P>')

    def __del__(self):
        self.cursor.close()
        self.conn.close()


def get_pic():
    url = 'http://www.wyssangyu.com/'
    picture = random.choice(os.listdir(DIR))
    url = url + 'img/novel/' + picture
    img_tag = f'<img src="{url}" alt="小说" />'
    return img_tag


def timestamp_to_str(timestamp=None, f='%Y-%m-%d %H:%M:%S'):
    if timestamp:
        time_tuple = time.localtime(timestamp)  # 把时间戳转换成时间元祖
        result = time.strftime(f, time_tuple)  # 把时间元祖转换成格式化好的时间
        return result
    else:
        return time.strptime(f)


def main(domain):
    c = Claim()
    num = c.get_num()
    count = int(COUNT)
    a = 0
    if not isinstance(count, int):
        raise Exception("===> 请把setting文件COUNT变量修改为数字! <===")
    for i in range(count):
        try:
            res = c.get_content(num)
            upload(domain, res[1], res[0], random.randint(1, 4))
            a += 1
        except Exception as e:
            print('===> 词条数据重复 词条数据略过 等待重新采集<===', e)
            count += 1
        else:
            present_time = timestamp_to_str(time.time())
            print(f'===> {domain} 成功上传{a}调数据 发布时间为{present_time} <===')
        time.sleep(30)


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=60) as exc:
        for i in DOMAIN:
            exc.submit(main, i)
    # main('www.wyssangyu.com')