# -*- coding: UTF-8 -*-
import requests


def upload(domain, title, content, cid):
    url = f'http://{domain}/collect/ApiUserHuochetou/articleAdd'
    data = {
        'password': 'lb976gp06vju',
        'title': title,
        'content': content,
        'cid': cid
    }
    response = requests.post(url, data=data)
    if len(response.text) > 2:
        raise Exception("该条数据上传失败")
    else:
        print(response.text)
