import datetime
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import xlwt
import pandas as pd


def main():
    url = "https://book.douban.com/latest?icn=index-latestbook-all"
    html = get_html(url)
    data = get_content(html)
    # print(data)
    # exit()
    df = pd.DataFrame(data, columns=['name', 'link', 'desc'])
    print(df)
    # save_to_excel(f"./新书速递{datetime.date.today()}.xls", data)
    # print("爬取完成")
    # input()


def get_content(html):
    bs = BeautifulSoup(html, 'html.parser')
    rules = {
        # "img": re.compile(r'<img src="(.*?)"/>'),
        "title": re.compile(r'<a href=".*?">(.*?)</a>'),
        "link": re.compile(r'<a href="(.*?)">.*?</a>'),
        "detail": re.compile(r'<p class="color-gray">.*?</p>.*?<p.*?>(.*?)</p>', re.S)
    }
    all = []
    for i in bs.select('#content li'):
        data = []
        for rule in rules:
            try:
                data.append(re.findall(rules[rule], str(i))[0].strip())
            except:
                continue
        all.append(data)
    return all


def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
        else:
            return None
    except RequestException:
        return None


def save_to_excel(path, data):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')

    title = ['图片', '书名', '链接', '描述']

    for i in title:
        ws.write(0, title.index(i), i)
    row = 1
    for i in data:
        for k in i:
            ws.write(row, i.index(k), k)
        row += 1
    wb.save(path)


if __name__ == '__main__':
    main()
