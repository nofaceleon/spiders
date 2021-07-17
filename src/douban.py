# 正则表达式
import random
import re
# 获取网页数据
import urllib.error
import urllib.request
# 网页解析
import bs4
from bs4 import BeautifulSoup
# excel
import xlwt
# 存入数据库
import sqlite3

# 爬取豆瓣图书信息存入excel


# 创建正则规则
findLink = re.compile(r'<a href="(.*?)">')
findImg = re.compile(r'<img .* src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findPeople = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

# searchRule = {
#     "link": {
#         "rule": findLink,
#         "msg": "影片链接"
#     },
#     "img": {
#         "rule": findImg,
#         "msg": "影片图片"
#     },
#     "title": {
#         "rule": findTitle,
#         "msg": "电影名称"
#     },
#     "rating": {
#         "rule": findRating,
#         "msg": "电影评分"
#     },
#     "people": {
#         "rule": findPeople,
#         "msg": "评分人数"
#     },
#     "inq": {
#         "rule": findInq,
#         "msg": "电影简介"
#     },
#     "bd": {
#         "rule": findBd,
#         "msg": "演员"
#     }
# }

searchRule2 = [
    {
        "flag": "link",
        "rule": findLink,
        "msg": "影片链接"
    },
    {
        "flag": "img",
        "rule": findImg,
        "msg": "影片图片"
    },
    {
        "flag": "title",
        "rule": findTitle,
        "msg": "电影名称"
    },
    {
        "flag": "rating",
        "rule": findRating,
        "msg": "电影评分"
    },
    {
        "flag": "people",
        "rule": findPeople,
        "msg": "评分人数"
    },
    {
        "flag": "inq",
        "rule": findInq,
        "msg": "电影简介"
    },
    # {
    #     "flag": "bd",
    #     "rule": findBd,
    #     "msg": "演员"
    # }
]


def main():
    baseUrl = "https://movie.douban.com/top250?start="
    fileName = "doubantop250-" + str(random.randint(1, 10000)) + ".xls"

    # 获取数据
    data = get_data(baseUrl)
    save_data(data, fileName)
    print("爬取完成")

    # 保存数据

    # html = ask_url(baseUrl)
    # bs = BeautifulSoup(html, "html.parser")
    #
    # t_list = bs.select('.hd a span')
    #
    # print(t_list)

    #
    # savePath = ".\\豆瓣电影Top250.xls"
    #
    # htmlInfo = getData(baseUrl)


# 获取数据
def get_data(baseurl):
    data = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = ask_url(url)
        data.append(get_html_info(html))
    return data


# 保存数据
def save_data(datas, path):
    workbook = xlwt.Workbook(encoding="utf-8")  # 创建对象
    worksheet = workbook.add_sheet('sheet1')  # 创建工作表

    for info in searchRule2:
        worksheet.write(0, searchRule2.index(info), info['msg'])

    i = 0
    for data in datas:
        for data_dict in data:
            lists = list(data_dict.values())
            for j in range(len(lists)):
                # print("i=%d,key=%d,v=%s", i, j, lists[j])
                worksheet.write(i + 1, j, lists[j])
            i = i + 1
    workbook.save(path)


# 提取html信息
def get_html_info(html):
    info = []
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="item"):
        data = {}  # 存储单个电影信息
        item = str(item)  # 转换成字符串
        for value in searchRule2:
            tmp = re.findall(value['rule'], item)
            if len(tmp) != 0:
                tmp = tmp[0].replace("。", "").replace("<br/>", "").replace(" ", "").replace("\n", "").strip()
            data[value["flag"]] = tmp
        info.append(data)
    # print(info)
    return info


# 获取网页数据
def ask_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        return html
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


def name_is_exists(tag):
    return tag.has_attr('name')


if __name__ == '__main__':
    main()
