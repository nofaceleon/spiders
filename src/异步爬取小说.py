import os
import time

import requests
import asyncio
import aiohttp
from aiohttp import TCPConnector
import aiofiles
from prettytable import PrettyTable
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import random

# 笔趣阁小说下载器
base_url = "https://www.xbiquge.la"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.212 Safari/537.36 "
}
EOL = '\n'

# 代理池
proxy = [
    {
        'http': 'http://14.115.107.63:808'
    },
    {
        'http': 'http://112.90.7.155:3128'
    },
    {
        'http': 'http://60.216.20.213:8001'
    },
    {
        'http': 'http://123.206.106.125:1081'
    },
    {
        'http': 'http://221.5.80.66:3128'
    },

]


def main():
    # get_book_content('cesces', "https://www.xbiquge.la/78/78062/31406094.html", './files')
    # exit()
    print("""
==================
  笔趣阁小说下载器
==================
""")

    key = input('输入搜索关键字(书名,作者名): ') or "天蚕土豆"
    resp = search(key)
    format_print(resp, {
        'index': '序号',
        'name': '书名',
        'author': '作者',
        'update_time': '更新时间',
        'url': '链接',
    })

    book_info = {}

    while True:
        try:
            index = input("输入序列号下载: ")
            book_info = [item for item in resp if item.get('index') == int(index)][0]
            if not book_info:
                print("参数输入错误, 请重新输入")
                continue
            break
        except:
            print("参数错误,请重新输入")
            continue
    # print(book_info['url'])
    # print(book_info['name'])
    # exit()
    book_dir = get_book_dir(book_info['url'])

    # os.system('cls')

    format_print(book_dir, {
        'index': '序号',
        'name': '章节',
        'url': '链接'
    })

    # confirm = input('是否确认下载?(1 确认) ')
    # if confirm != '1':
    #     exit()

    print(
        """
0. 取消
1. 同步下载 (速度慢,成功率高)
2. 多线程下载 (并发高容易503)
3. 异步协程下载 (并发高容易503)
        """
    )

    start = 0
    while True:
        download_type = input('选择下载方式: ')
        if download_type == '0':
            print("取消下载")
            exit()
        path = f'./files/{book_info["name"]}'
        if not os.path.exists(path):
            os.makedirs(path)

        if download_type == '1':
            start = time.time()
            sync_download(book_dir, path)
            break
        elif download_type == '2':
            start = time.time()
            multi_download(book_dir, path)
            break
        elif download_type == '3':
            start = time.time()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(download(book_dir=book_dir, path=path))
            # asyncio.run(download(book_dir=book_dir, path=path))
            break
        else:
            print("输入错误")
            continue

    end = time.time()
    print(f'下载完成,总耗时{end - start}')

    # 同步下载

    # for i in book_dir:
    #     title = i['name']
    #     url = i['url']
    #     get_book_content(title, url, path)
    # break

    # 开启异步协程下载
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(download(book_dir=book_dir, path=path))
    # asyncio.run(download(book_dir=book_dir, path=path))

    # 开启多线程下载 (当前网站支持的并发数量太少,容易503)
    # with ThreadPoolExecutor(2) as t:
    #     for i in book_dir:
    #         title = i['name']
    #         url = i['url']
    #         t.submit(get_book_content, title=title, url=url, path=path)


# 搜索页面
def search(key):
    search_url = "https://www.xbiquge.la/modules/article/waps.php"
    r = requests.post(search_url, data={"searchkey": key}, headers=headers)
    r.encoding = 'utf-8'
    tree = etree.HTML(r.text)
    trs = tree.xpath('//table[@class="grid"]/tr[position()>1]')
    index = 1
    search_res_l = []
    for tr in trs:
        tmp_dic = {
            "index": index,
            "name": tr.xpath('./td[1]/a/text()')[0],
            "author": tr.xpath('./td[3]/text()')[0],
            "update_time": tr.xpath('./td[4]/text()')[0].strip(),
            "url": tr.xpath('./td[1]/a/@href')[0]
        }
        index += 1
        search_res_l.append(tmp_dic)
    return search_res_l


# 获取图书目录
def get_book_dir(book_url):
    r = requests.get(book_url, headers=headers)
    r.encoding = 'utf-8'
    tree = etree.HTML(r.text)
    dds = tree.xpath('//div[@id="list"]/dl/dd')
    all_l = []
    index = 1
    for dd in dds:
        dic_tmp = {
            'index': index,
            'name': dd.xpath('./a/text()')[0],
            'url': base_url + dd.xpath('./a/@href')[0]
        }
        all_l.append(dic_tmp)
        index += 1
    return all_l


# 美化输出
def format_print(resp, col):
    x = PrettyTable()
    x.field_names = list(col.values())
    for item in resp:
        tmp = [item[k] for k in col.keys()]
        x.add_row(tmp)
    print(x)


# 同步的方式下载 效率极低
def get_book_content(title, url, path):
    # 添加代理测试
    r = requests.get(url, headers=headers, timeout=10, proxies=random.choice(proxy))
    if r.status_code != 200:
        print("状态码不对" + str(r.status_code))
        return None
    r.encoding = 'utf-8'
    tree = etree.HTML(r.text)
    content = tree.xpath('//div[@id="content"]/text()')
    # print(content)
    data = [i.replace('\xa0', '').replace('\r', '') for i in content]
    with open(f'{path}/{title}.txt', 'w+', encoding='utf-8') as f:
        f.write(title)
        for i in data:
            f.write(i)
    print(f'{title}---下载完成')
    # time.sleep(random.randint(1, 3))


async def a_get_book_content(title, url, path):
    conn = TCPConnector(limit=5)  # 控制并发
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(url) as r:
            tree = etree.HTML(await r.text())
            content = tree.xpath('//div[@id="content"]/text()')
            # print(content)
            data = [i.replace('\xa0', '').replace('\r', EOL) for i in content]
            data.insert(0, title + EOL)
            datas = "".join(data)
            # print(data)
            async with aiofiles.open(f'{path}/{title}.txt', 'w+', encoding='utf-8') as f:
                await f.write(datas)
                # for i in data:
                #     await f.write(i)
                print(f'{title}---下载完成')

    # await asyncio.sleep(1)


# 异步下载数据
async def download(book_dir, path):
    tasks = []
    for i in book_dir:
        title = i['name']
        url = i['url']
        tasks.append(asyncio.create_task(a_get_book_content(title, url, path)))
    await asyncio.wait(tasks)


# 同步下载数据
def sync_download(book_dir, path):
    for i in book_dir:
        title = i['name']
        url = i['url']
        get_book_content(title, url, path)
        time.sleep(random.randint(1, 3))  # 控制频率


# 多线程下载
def multi_download(book_dir, path):
    # 开启多线程下载 (当前网站支持的并发数量太少,容易503)
    with ThreadPoolExecutor(2) as t:
        for i in book_dir:
            title = i['name']
            url = i['url']
            t.submit(get_book_content, title=title, url=url, path=path)


if __name__ == '__main__':
    main()
