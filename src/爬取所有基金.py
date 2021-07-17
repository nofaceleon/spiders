import re
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd


def main():
    base_url = "http://fund.eastmoney.com/allfund.html"
    html = get_html(base_url)
    data = get_content(html)
    save_data(data)
    print('done')


def get_html(base_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 ",
    }
    try:
        r = requests.get(base_url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'gbk'
            return r.text
        else:
            print(f"错误:{r.status_code}")
    except RequestException:
        print("请求异常")
        exit()


def get_content(html):
    filter = {
        "name": re.compile('<li .*?><div><a href=".*?">（.*?）(.*?)</a>.*?</div></li>'),
        "code": re.compile('<li .*?><div><a href=".*?">（(.*?)）.*?</a>.*?</div></li>'),
        "link": re.compile(
            '<li .*?><div><a href="(.*?)">.*?</div></li>')
    }

    bs = BeautifulSoup(html, 'html.parser')
    data_l = bs.find_all('li', class_="b")
    final_l = []
    for i in data_l:
        tmp = {}
        for k in filter:
            info = re.findall(filter[k], str(i))
            if len(info) != 0:
                info = info[0]
            tmp[k] = info
        final_l.append(tmp)
    return final_l


def save_data(data):
    df = pd.DataFrame(data)
    print(df)
    # df.to_excel('./files/天天基金所有基金代码.xlsx', encoding='utf-8_sig')  # 防止乱码


if __name__ == '__main__':
    main()
