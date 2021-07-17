import hashlib
import hmac
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.212 Safari/537.36 ",
}


def main():
    print("""
=========================================
蜻蜓FM音频下载器(只能下载免费内容)
使用方法:
例如,专辑页面地址为 https://www.qingting.fm/channels/124982
则专辑ID为 124982
=========================================
    """)
    while True:
        album_id = input('输入蜻蜓FM专辑ID (0 退出): ')
        if album_id == '0':
            print('bye')
            exit()
        if not album_id:
            print("ID不能为空")
        else:
            break
    start = time.time()
    album_name, dir_list = get_dir_list(album_id)
    count = len(dir_list)
    confirm = input(f"{album_name},总共{count}集, 是否开始下载?(1 确认)") or '0'

    if confirm != '1':
        exit()

    path = f'./files/{album_name}/'
    if not os.path.exists(path):
        os.makedirs(path)
    index = 1
    with ThreadPoolExecutor(5) as t:
        for i in dir_list:
            t.submit(download_m4a, api=build_api_url(album_id, i['song_id']), path=path,
                     filename='[' + str(index) + ']' + i['name'])
            # download_m4a(build_api_url(album_id, i['song_id']), path, '[' + str(index) + ']' + i['name'])
            index += 1
        # print(f"{i['name']}---下载完毕")
    end = time.time()
    print(f"下载完成总耗时: {end - start}秒")


def get_dir_list(album_id):
    page = 1
    limit = 30
    url = "https://webbff.qingting.fm/www"
    base_headers = {
        'authority': 'i.qingting.fm',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'origin': 'https://www.qingting.fm',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.qingting.fm/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=707c9fd816236825574815499e22ecb82996e49908614154f3230c9e753c8a'
    }

    dir_list = []

    while True:
        payload = json.dumps({
            "query": "{channelPage(cid:" + str(
                album_id) + ",page:" + str(
                page) + ",order:\"asc\",qtId:\"null\"){album\n        seo\n        plist\n        reclist\n        categoryId\n        categoryName\n        collectionKeywords\n      }\n    }"
        })

        r = requests.post(url, headers=base_headers, data=payload)
        data = r.json()
        album_name = data['data']['channelPage']['album']['name']
        plist = data['data']['channelPage']['plist']
        for i in plist:
            dir_list.append({
                'name': i['name'],
                'song_id': i['id']
            })
        print(f"获取专辑列表--第{page}页")
        program_count = data['data']['channelPage']['album']['program_count']  # 获取专辑总数
        current_count = int(page * limit)
        if current_count >= program_count:
            break
        else:
            page += 1
    return album_name, dir_list


# 音频下载
def download_m4a(api, path, filename):
    r = requests.get(api, headers=headers, allow_redirects=False)
    if r.status_code == 302:
        media_url = r.headers.get('Location')
        if media_url:
            media = requests.get(media_url, headers=headers)
            with open(f'{path}/{filename}.m4a', 'wb') as f:
                f.write(media.content)
            print(f"{filename}---下载完毕")
        else:
            print(f"{filename}---未获取到链接")
    else:
        print(f"{filename}---下载失败")


# 获取音频下载链接
def build_api_url(album_id, song_id):
    timestamp = int(time.time() * 1000)
    # 加密字符串
    strs = f"/audiostream/redirect/{album_id}/{song_id}?access_token=&device_id=MOBILESITE&qingting_id=&t={timestamp}"
    key = b"fpMn12&38f_2e"  # 加密密钥
    sign = hmac.new(key, strs.encode('utf-8'), hashlib.md5).hexdigest()
    api_url = f"https://audio.qingting.fm/audiostream/redirect/{album_id}/{song_id}?access_token=&device_id=MOBILESITE&qingting_id=&t={timestamp}&sign={sign}"
    return api_url


if __name__ == '__main__':
    while True:
        main()
