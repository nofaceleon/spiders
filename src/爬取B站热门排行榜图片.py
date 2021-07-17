import datetime
import os
import re
import requests
from requests.exceptions import RequestException
import redis
import json
import pandas as pd
import sendMail

url = "https://api.bilibili.com/x/web-interface/popular?ps=20&pn="
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.212 Safari/537.36 "
}


def save_title_img():
    page = 0
    path = "./哔哩哔哩热门排行榜图片/" + str(datetime.date.today())
    if not os.path.exists(path):
        os.makedirs(path)
    while 1:
        page += 1
        print(page)
        data_json = get_url(url + str(page))
        lists = get_hot_title(data_json)
        for i in lists:
            # title = str(i['title']).strip() \
            #     .replace("丨", ",") \
            #     .replace("?", '') \
            #     .replace("|", ",") \
            #     .replace("/", ",") \
            #     .replace('"', '') \
            #     .replace('，', '')

            title = re.sub("[丨?|/\",，]", "", str(i['title']))
            file_name = f"{path}/{title}.jpg"
            with open(file_name, "wb") as f:
                f.write(requests.get(i['pic']).content)

        if data_json['data']['no_more']:
            break
    print("获取完毕")


def main():
    key = "bilibliRank"
    flag = True
    page = 0
    rd = redis.Redis(host='localhost', port='6379', decode_responses=True)
    rd.delete(key)
    while flag:
        page += 1
        print(page)
        data_json = get_url(url + str(page))
        lists = get_hot_title(data_json)
        save_to_redis(lists, key, rd)
        if data_json['data']['no_more']:
            break
    print("获取完毕")


def mail():
    page = 0
    total_l = []
    while 1:
        page += 1
        print(page)
        data_json = get_url(url + str(page))
        total_l.extend(get_hot_title(data_json))
        if data_json['data']['no_more']:
            break

    df = pd.DataFrame(total_l)
    # res = sendMail.send_email('哔哩哔哩热门', df.to_html(escape=False, render_links=True))
    print(df)


def get_url(base_url):
    try:
        r = requests.get(base_url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.json()
    except RequestException:
        return None


def get_hot_title(data):
    all_list = []
    for i in data['data']['list']:
        tmp = {
            'pic': f'<img src="{i["pic"]}" style="width:206px;height:auto"/>',
            "title": i['title'],
            # "desc": i['desc'],
            "up": i['owner']['name'],
            "recommend": i['rcmd_reason']['content'],
            "tag": i['tname'],
            'link': i['short_link']
        }
        all_list.append(tmp)
    return all_list


def save_to_txt(data, file_name):
    f = open(file_name, "a+", encoding='utf-8')
    for i in data:
        data_str = "标题:" + i['title']
        f.write(data_str + "\n")
    f.close()


# 保存数据到 excel
def save_to_excel():
    pass


def save_to_redis(lists, redis_key, rd):
    for i in lists:
        rd.lpush(redis_key, json.dumps(i))


if __name__ == '__main__':
    # main()
    # save_title_img() # 爬取数据保存图片到本地
    mail()  # 爬取数据并发送邮件
