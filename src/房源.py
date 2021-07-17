import requests
from lxml import etree

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Host': 'shenzhen.qfang.com',
    'Connection': 'keep-alive'
}

url = 'https://shenzhen.qfang.com/sale'
rsp_3 = requests.get(url=url, headers=headers)
print(rsp_3.text)
exit()
selector = etree.HTML(rsp_3.text)
x = selector.xpath('/html/body/div[4]/div/div[1]/div[4]/ul/li[1]/div[2]/div[1]/a/text()')
print(x)
