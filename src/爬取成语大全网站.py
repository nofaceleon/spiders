import time

import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import aiofiles
import asyncio

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.212 Safari/537.36 "
}

domain = "http://chengyu.t086.com"
sem = asyncio.Semaphore(10)  # 控制并发度


def main():
    for i in range(ord('A'), ord('Z') + 1):
        total_urls = get_one_all_detail_urls(chr(i))
        # 拿到所有链接开始异步协程下载保存
        # 取得了所有的链接,开启异步协程下载
        loop = asyncio.get_event_loop()
        loop.run_until_complete(a_download(urls=total_urls))
        print(f"{chr(i)}_--爬取完毕")


def main_old():
    # start = time.time()

    for i in range(ord('A'), ord('Z') + 1):
        page = 1
        while True:
            url = f"http://chengyu.t086.com/list/{chr(i)}_{page}.html"
            have_next_page = save_one_page(url)
            print(f"{chr(i)}_{page}--爬取完毕")
            if not have_next_page:
                break
            page += 1


def save_one_page(url):
    # url = "http://chengyu.t086.com/list/A_1.html"
    # url = "http://chengyu.t086.com/list/F_14.html"
    html = get_html(url)
    if not html:
        return False
    tree = etree.HTML(html)
    have_next_page = False
    next_page = (tree.xpath('//div[@class="mainbar3"]/div[@class="a2"]/a[last()]/text()') + ['无'])[0]
    if next_page == '下一页':
        have_next_page = True

    lis = tree.xpath('//div[@class="listw"]/ul/li')
    detail_urls = []
    for l in lis:
        detail_urls.append(domain + l.xpath('./a/@href')[0])

    # 拿到了这个页面的所有的成语的链接
    page_content = []
    with ThreadPoolExecutor(50) as t:
        for u in detail_urls:
            tmp = t.submit(save_detail, u)
            page_content.append(tmp.result())
    titles = list(page_content[0].keys())
    with open('../files/成语大全(完整).csv', 'a+', encoding='utf_8_sig') as f:  # utf_8_sig 防止excel打开的时候乱码
        f_csv = csv.DictWriter(f, titles)
        f_csv.writerows(page_content)
    print(f"{url}---保存完毕")

    return have_next_page
    # 判断是否有下一页


def get_html(url):
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"状态码异常{r.status_code}")
        return None
    else:
        r.encoding = 'gbk'
        return r.text


# ===========协程模式总是不成功=====================

def get_one_all_detail_urls(i):
    page = 1
    total_detail_urls = []
    while True:
        url = f"http://chengyu.t086.com/list/{i}_{page}.html"
        html = get_html(url)
        tree = etree.HTML(html)
        lis = tree.xpath('//div[@class="listw"]/ul/li')
        for l in lis:
            total_detail_urls.append(domain + l.xpath('./a/@href')[0])

        next_page = (tree.xpath('//div[@class="mainbar3"]/div[@class="a2"]/a[last()]/text()') + ['无'])[0]
        if next_page != '下一页':
            break
        else:
            page += 1
    return total_detail_urls


# 协程方式下载数据
async def a_download(urls):
    tasks = []
    # sem = asyncio.Semaphore(5)  # 控制并发
    for i in urls:
        tasks.append(asyncio.create_task(a_save_detail(i)))  # 添加异步协程任务
    await asyncio.wait(tasks)


# 协程方式保存单个链接的数据
async def a_save_detail(url):
    async with sem:  # 控制并发度
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as r:
                tree = etree.HTML(await r.text(encoding='gbk'))
                table = tree.xpath('//div[@id="main"]/table[1]')[0]
                tmp = {
                    'name': (table.xpath('./tr[1]/td[last()]/h1/text()') + ['无'])[0],  # 词名
                    'faying': (table.xpath('./tr[2]/td[last()]/text()') + ['无'])[0],  # 发音
                    'paraphrase': (table.xpath('./tr[3]/td[last()]/text()') + ['无'])[0],  # 释义
                    'from': (table.xpath('./tr[4]/td[last()]/text()') + ['无'])[0],  # 出处
                    'example': "".join(table.xpath('./tr[5]/td[last()]/text()'
                                                   '|./tr[5]/td[last()]/*/text()')),
                    'like': (table.xpath('./tr/td/span[@id="hits"]/text()') + ['无'])[0],
                }
                async with aiofiles.open('../files/成语大全协程版本.txt', 'a+', encoding='utf-8') as f:
                    await f.write(",".join(list(tmp.values()) + ['\n']))


# 获取单页数据
def save_detail(url):
    # print(url)
    html = get_html(url)
    tree = etree.HTML(html)
    table = tree.xpath('//div[@id="main"]/table[1]')[0]
    tmp = {
        'name': (table.xpath('./tr[1]/td[last()]/h1/text()') + ['无'])[0],  # 词名
        'faying': (table.xpath('./tr[2]/td[last()]/text()') + ['无'])[0],  # 发音
        'paraphrase': (table.xpath('./tr[3]/td[last()]/text()') + ['无'])[0],  # 释义
        'from': (table.xpath('./tr[4]/td[last()]/text()') + ['无'])[0],  # 出处
        'example': "".join(table.xpath('./tr[5]/td[last()]/text()'
                                       '|./tr[5]/td[last()]/*/text()')),
        'like': (table.xpath('./tr/td/span[@id="hits"]/text()') + ['无'])[0],
    }
    # print(tmp)
    return tmp
    #
    # detail = []
    # name = table.xpath('./tr/td[position()>1]/h1/text()')
    # faying = table.xpath('./tr/td[position()>1]/h1/text()')
    # print(name)


if __name__ == '__main__':
    start = time.time()
    main_old()
    # main()
    end = time.time()
    print(f"爬取完成,总耗时:{end - start}")
