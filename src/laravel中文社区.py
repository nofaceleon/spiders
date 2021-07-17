import time

import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


def main():
    start = time.time()
    with ThreadPoolExecutor(20) as t:
        for i in range(1, 29):
            url = f"https://learnku.com/laravel?page={i}"
            t.submit(save_info, url=url, page=i)
    end = time.time()

    print(f"down---{end - start}")
    # html = get_html()
    # # print(html)
    # get_content(html)


def save_info(url, page):
    get_content(get_html(url))
    # print(f"第{page}页,爬取完毕")


def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        print(f'状态码错误{r.status_code}')


def get_content(html):
    tree = etree.HTML(html)
    # total_page = tree.xpath('//ul[@class="pagination"]/li[last()-1]/a/text()')[0]
    # if not total_page:
    #     print("未获取到页码信息")
    #     exit()
    # spans = tree.xpath('//span[@class="topic-title"]')
    divs = tree.xpath('//div[@class="py-2 simple-topic"]')

    for i in divs:
        title = i.xpath('./a/span[@class="topic-title"]/text()')[0].strip()
        link = i.xpath('./a/@href')[0]
        if title:
            print(title)
            print(link)
            print("=" * 20)


# with open('./files/laravel_info3.txt', 'a+', encoding='utf-8') as f:
#     for i in spans:
#         title = i.xpath('./text()')[0].strip()
#         if title:
#             f.write(title + '\n')


if __name__ == '__main__':
    main()
