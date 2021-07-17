import time

import requests
import os
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor  # 使用线程池

# 爬取懂车帝所有汽车图片

# 图片保存路径
path = "./all_cars_img/"


def main():
    offset = 1
    limit = 30
    while 1:
        print(f"第{offset}页")
        data = {
            "offset": offset,
            "limit": limit,
            "is_refresh": 0,
            "city_name": "合肥"
        }
        base_url = "https://www.dongchedi.com/motor/pc/car/brand/get_select_series"
        data_json = get_url(base_url, data)
        if not os.path.exists(path):
            os.makedirs(path)
        for i in data_json['data']['series']:
            outter_name = str(i['outter_name']).replace("/", "").replace("\t", "").replace(" ", "")
            with open(f"{path}{outter_name}.png", "wb") as img:
                img.write(requests.get(i['cover_url']).content)
        if not data_json['data']['series']:
            break
        offset += 1

    print("爬取完毕")


def get_url(base_url, data):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    try:
        r = requests.post(base_url, data=data, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except RequestException:
        return None


def thread_main(offset):
    limit = 30
    print(f"第{offset}页")
    data = {
        "offset": offset,
        "limit": limit,
        "is_refresh": 0,
        "city_name": "合肥"
    }
    base_url = "https://www.dongchedi.com/motor/pc/car/brand/get_select_series"
    data_json = get_url(base_url, data)
    if not os.path.exists(path):
        os.makedirs(path)
    for i in data_json['data']['series']:
        outter_name = str(i['outter_name']).replace("/", "").replace("\t", "").replace(" ", "")
        with open(f"{path}{outter_name}.png", "wb") as img:
            img.write(requests.get(i['cover_url']).content)


if __name__ == '__main__':
    # main()
    start = time.time()
    # 开启50个线程
    with ThreadPoolExecutor(50) as t:
        for i in range(1, 110):
            t.submit(thread_main, i)
    end = time.time()
    print("总共完成时间%d" % int(end - start))
