import re
import time

import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.212 Safari/537.36 "
}

book_url = 'https://www.shizongzui.cc/qinshu/'


def main():
    start = time.time()
    html = get_html(book_url)
    book_name, links = get_dir(html)
    book_name = re.sub("[丨?|/\",，:：]", "", book_name)
    download_path = f"./{book_name}/"

    if links:
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        with ThreadPoolExecutor(10) as t:
            for i in links:
                t.submit(get_book_content, i['link'], download_path)
    end = time.time()
    print(f'全部下载完成:{end - start}')


def get_html(url):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        return r.text
    else:
        print(f"状态码:{r.status_code}")


def get_dir(html):
    tree = etree.HTML(html)
    book_name = tree.xpath('//div[@class="v"]/h1/text()')[0]
    buffer = []
    links = tree.xpath('//div[@class="booklist clearfix"]/span[position()>1]/a')
    for i in links:
        buffer.append({
            'name': i.xpath('./text()')[0],
            'link': i.xpath('./@href')[0]
        })
    return book_name, buffer


def get_book_content(url, download_path):
    html = get_html(url)
    tree = etree.HTML(html)
    content = tree.xpath('//div[@id="BookText"]/text()')
    content = [i.replace('\u3000', ' ') for i in content]
    content = "\n".join(content)
    filename = tree.xpath('//div[@class="chaptertitle clearfix"]/h1/text()')[0].replace(' ',
                                                                                        '_') + '.txt'
    filename = re.sub("[丨?|/\",，:：]", "", filename)
    with open(download_path + filename, 'w+', encoding='utf-8') as f:
        f.write(content)
    print(f"{filename}保存完毕")


if __name__ == '__main__':
    main()
