import json
import requests
from requests.exceptions import RequestException
from Crypto.Cipher import AES
from base64 import b64encode
import pandas as pd
import re

"""
cursor: -1
offset: 0
orderType: 1
pageNo: 1
pageSize: 20
rid: "R_SO_4_36392029"
threadId: "R_SO_4_36392029"


 function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }

   function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }


window.asrsea(JSON.stringify(i8a), bwa9R(["流泪", "强"]), bwa9R(RQ4U.md), bwa9R(["爱心", "女孩", "惊恐", "大笑"]))
function d(d, e, f, g) { 
        var h = {} , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        :return h
    }

"""

# 定值
e = "010001"

# 定值
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"

# 定值
g = "0CoJUm6Qyw8W8jud"

# 定值
i = "Yab6WAtcfEn43ye3"

encSecKey = "414ea241651795194f192cf02b9c2f98e8f1c54cf1a922653403087f86617c9bc7455b80124cb4ddbefc10e59c9d488b08fa83ebb6d761e772cc7c172c20986373945f9d064e799d5693b56c1544e84fdc6b729e3e7d834a89c3d1e21f3980130bbd9c944e123527d362d0ca35bc04d78dc9cbb5362d6ae7155cb527bd6d6748"


# params = {
#     "encSecKey": "43f1a7fe1d42ecdb1213ea8dd91af356033e45938070dead58eabdb8a3f07d98669805bb8ef8d9ad5a51258cde0994b5422c95c6268ac05e9be3e0d0d0fb66494ea3a1a1249817230dff9d8904027da0b91d87c08a6b18b2310f79906aa9e681ac351f6668d2e07352ba03418ed14808f6b7ace6970748444e5749caa1c0c119",
#     "encText": "/mCDWalAo+wpM9IBCF/d5zJsy1nvHUxyr/Ewy4qHkoK4G5HffDsOQ2KWVE6Lew8x53M7a0CcoRep8HwoG5Stf2lPGpEBR45V9exJ/P7gNm2xL9DcqmYhVvZWD8L7eoEE"
#
# }


def get_encText(data):
    first = aes(data, g)
    second = aes(first, i)
    return second


# aes加密补齐16位
# def add_to_16(text):
#     if len(text.encode('utf-8')) % 16:
#         add = 16 - (len(text.encode('utf-8')) % 16)
#     else:
#         add = 0
#     text = text + ('\0' * add)
#     return text.encode('utf-8')

# aes加密补齐16位
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def aes(text, key):
    key = key.encode('utf-8')
    iv = '0102030405060708'.encode('utf-8')  # 偏移量
    # text = add_to_16(text)
    text = to_16(text)
    cryptos = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
    cipher_text = cryptos.encrypt(text.encode('utf-8'))
    return str(b64encode(cipher_text), "utf-8")


def main():
    print("{:=^30}".format('获取网易云歌曲热评'))
    while True:
        song_id = input('请输入歌曲ID(输入0退出): ')
        if song_id == '':
            print("歌曲ID不能为空!")
            continue
        if song_id == '0':
            print('Bye')
            break
        # song_id = '402073808'
        # song_id = '36392029'
        # 请求参数

        # print(resp)
        music_name = get_music_name(song_id)
        print(music_name)
        resp = get_hot_comments(song_id)
        data_l = get_content(resp)
        df = pd.DataFrame(data_l)
        # df.to_excel('./files/网易云.xlsx')
        print(df)


def get_hot_comments(song_id):
    url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
    d = {
        "cursor": "-1",
        "offset": "0",
        "orderType": "1",
        "pageNo": "1",
        "pageSize": "20",
        "rid": f"R_SO_4_{song_id}",
        "threadId": f"R_SO_4_{song_id}",
    }

    # 第二页数据
    # d = {
    #     "cursor": "-1",
    #     "offset": "40",
    #     "orderType": "1",
    #     "pageNo": "2",
    #     "pageSize": "20",
    #     "rid": "R_SO_4_36392029",
    #     "threadId": "R_SO_4_36392029",
    # }

    data = {
        "params": get_encText(json.dumps(d)),
        "encSecKey": encSecKey
    }
    resp = get_url(data=data, url=url, method='POST', type='json')
    return resp


def get_url(url, data=None, method='GET', type='html'):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    try:
        if method == 'POST':
            r = requests.post(url, data=data, headers=headers)
        elif method == 'GET':
            r = requests.get(url, headers=headers)
        else:
            r = requests.get(url, headers=headers)
        if r.status_code == 200:
            if type == 'json':
                return r.json()
            elif type == 'html':
                return r.text
        else:
            return None
    except RequestException:
        return None


# 获取热门评论
def get_content(data):
    data_l = []
    for item in data['data']['hotComments']:
        tmp = {
            '昵称': item['user']['nickname'],
            '评论': item['content'].strip().replace('\n', ''),
        }
        data_l.append(tmp)
    return data_l


def get_music_name(song_id):
    url = f"https://music.163.com/song?id={song_id}"
    resp = get_url(url=url, method='GET', type='html')
    title = re.findall('<title>(.*?)</title>', resp)[0]
    return title


if __name__ == '__main__':
    main()
