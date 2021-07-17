import random
import time

import requests
from lxml import etree
import pandas as pd



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
    for i in range(1, 2):
        url = f"https://www.lagou.com/shanghai-zhaopin/PHP/{i}/?filterOption=2&sid=69a2a0af6b804799852fc352f927ba53"
        go(url)
        print(f"第{i}页爬取完毕")
        time.sleep(random.randint(1, 3))  # 防止被限制IP
    print("down")


def go(url):
    headers = {
        'authority': 'www.lagou.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.lagou.com/common-sec/security-check.html?seed=851A61BCA6E633053A00DF9F2F6365009DED4FB528BCB9828E8BB4B09C60EB7CF3345714CB7624DA1F37E755880FE3A5&ts=16231496072670&name=ece700ff7792&callbackUrl=https%3A%2F%2Fwww.lagou.com%2Fshanghai-zhaopin%2FPHP%2F%3FlabelWords%3Dlabel&srcReferer=https%3A%2F%2Fwww.lagou.com%2F',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'user_trace_token=20210210111209-df3bea08-584b-4cd5-93b7-c98ced77fd94; LGUID=20210210111210-c9963b64-cefe-4cae-9736-f9bac393a5f0; _ga=GA1.2.2140429521.1612926731; RECOMMEND_TIP=true; index_location_city=%E4%B8%8A%E6%B5%B7; JSESSIONID=ABAAAECABFAACEAEF7E2F4B46350A80C5304A446C7E727A; WEBTJ-ID=2021068%E4%B8%8B%E5%8D%886:53:25185325-179eb4172e977e-061d2c5c22e6ed-f7f1939-2073600-179eb4172eb721; X_HTTP_TOKEN=15fb14547ef1ad6060694132614d18b5774dfd8b1a; PRE_UTM=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; privacyPolicyPopup=false; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1622194461,1623053194,1623149606; _gid=GA1.2.745178365.1623149606; LGSID=20210608185326-53ce6e2b-91c9-49d3-9ed4-234816e1ca1b; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DLUu-N74KBtONrMSKpJliiSNRLTia6EBlaU67tvyNxvi%26wd%3D%26eqid%3Db2cc9b310008119a0000000660bf4c24; sensorsdata2015session=%7B%7D; TG-TRACK-CODE=index_navigation; __lg_stoken__=ece700ff77926755c3031dd65b585fc315841ab588a654c79a9196718a9aaff2bb4a81827cb70e19cf4d876074956a5b1db89d8623d4efb5b1660467ae792de816f0dc6464df; SEARCH_ID=a3364e8f1b0a4b00a72269c834887983; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217789ecc2461c6-0e41fc96ecdb9d-53e3566-2073600-17789ecc248940%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2291.0.4472.77%22%7D%2C%22%24device_id%22%3A%2217789ecc2461c6-0e41fc96ecdb9d-53e3566-2073600-17789ecc248940%22%7D; _gat=1; LGRID=20210608191751-ccff3081-7deb-477c-9cb6-61f038bf6dfd; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1623151071; X_HTTP_TOKEN=42daf4b72327b2813901513261bf5e71415983ed09; SEARCH_ID=ef0b2df1e0d64895b857eac4d8bf1d1c'
    }

    r = requests.get(url, headers=headers, proxies=random.choice(proxy))
    # //li[@class="con_list_item default_list"]
    if r.status_code != 200:
        print(f"状态码错误{r.status_code}")

    tree = etree.HTML(r.text)
    lis = tree.xpath('//div[@class="list_item_top"]')
    data = []
    for l in lis:
        tmp = {
            '职位名称': l.xpath('./div[@class="position"]/div[@class="p_top"]/a/h3/text()')[0],
            '薪水': l.xpath('./div[@class="position"]/div[@class="p_bot"]/div/span/text()')[0],
            '经验': l.xpath('./div[@class="position"]/div[@class="p_bot"]/div/text()')[-1].strip(),
            '公司名称': l.xpath('./div[@class="company"]/div[@class="company_name"]/a/text()')[0],
            '地区': l.xpath('./div[@class="position"]/div[@class="p_top"]/a/span/em/text()')[0]
        }
        # print(tmp)
        data.append(tmp)

    with open('../files/PHP拉钩信息111.txt', 'a+', encoding='utf-8') as f:
        for i in data:
            f.write(",".join(list(i.values())) + '\n')
            # f.write('')

    # df = pd.DataFrame(data)
    # df.to_csv('./files/上海PHP拉钩招聘信息.csv', mode='a', encoding="utf_8_sig", header=False)


if __name__ == '__main__':
    main()
