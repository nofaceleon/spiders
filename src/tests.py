import requests

from lxml import etree

url = "https://www.qidian.com/all?action=1&orderId=&page=1&vip=0&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}
# 拿到主页的源代码
resp = requests.get(url, headers=headers)
# 拿主页的源代码进行xpath
html = etree.HTML(resp.text)
# 拿到主页面下的小说的url地址
page = html.xpath('//div[@class="book-img-box"]/a/@href')[0]
# 主页面的书本的内容的小说的名字
novel_name = html.xpath('//div[@class="book-mid-info"]/h4/a/text()')[0]
# 获得实际地址
link = "https:" + page
# print(link)
data = requests.get(link, headers=headers)
# 再进入单部小说进行访问
html = etree.HTML(data.text)

# 选到目录的的章节
# print("小说名字是：", novel_name)
sec_url = html.xpath('//ul[@class="cf"]/li/a/@href')
cur_sec = 0
for cur_url in sec_url:
    # print(cur_url)

    # 小说章节

    novel_section = html.xpath('//ul[@class="cf"]/li/a/text()')
    # print(novel_section)
    # 转换为实际章节地址 并进行访问 输出源代码
    page = requests.get("https:" + cur_url, headers=headers)
    # print(page.text)

    # 把源代码进行xpath定位 获取到小说内容
    res = etree.HTML(page.text)
    # print(page.text)
    content = res.xpath('//div[@class="read-content j_readContent"]/p/text()')
    # 转换为字符串
    content = " ".join(content)

    # print("小说章节是：", novel_section)
    print("当前小说的名字是 %s , 当前小说的章节是 %s , 当前章的内容是的内容是：\n%s\n\n, " % (novel_name, novel_section[cur_sec], content))
    cur_sec += 1