# -*- coding: UTF-8 -*-
import requests


def seo_api(content):
    data = {
        'content': content,
        'ratio': 30
    }
    response = requests.post('http://www.seowyc.com/seo/api/wyc.html', data=data, timeout=6)
    c = response.json()['content'].strip()
    return c


if __name__ == '__main__':
    result = seo_api('我是蛇啊')
    print(result)
