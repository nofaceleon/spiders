import requests
from lxml import etree
from requests.exceptions import RequestException
import xlwt
import datetime
import pandas as pd
import sendMail
# 防止报错
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    data = get_content(get_html('https://news.ceic.ac.cn/'))
    df = pd.DataFrame(data[1:], columns=data[:1][0])
    print(df)
    # sendMail.send_email('地震信息', df.to_html())
    # print('done')

    # df.to_html('./files/dizheng.html', encoding='utf-8')
    # print(df)
    # # save_data(data)
    # print("爬取完成")


def get_html(base_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 ",
    }

    try:
        r = requests.get(base_url, headers=headers, verify=False)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        else:
            print(f"请求失败{r.status_code}")
            exit()
    except RequestException as e:
        print("异常")
        exit()


def get_content(html):
    tree = etree.HTML(html)
    all_l = tree.xpath('//div[@class="news-content"]/table/tr/*/text()'
                       '| //div[@class="news-content"]/table/tr/*/a/text()')
    tmp = []
    for i in range(0, len(all_l), 6):
        tmp.append(all_l[i:i + 6])
    return tmp


def save_data(data):
    today = datetime.date.today()
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')
    row = 0
    for i in data:
        for v in i:
            ws.write(row, i.index(v), v)
        row += 1
    wb.save(f"./今日地震信息{today}.xls")


if __name__ == '__main__':
    main()
