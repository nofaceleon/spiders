import requests
from lxml import etree
import csv
import pandas as pd

# 备案的颜色
# background_color = "#96E686"
background_color = "#F0FFB6"


def main():
    html = get_html(
        "http://www.ahscfdc.com/web/houseinfo/ShowBuildSaleInfo.aspx?BuildingID=A3FB4yc1MK3m%2fVIBrEzcidUnEoi4bgZklvqXFILZKqDUlu2MWpTVog%3d%3d")

    tree = etree.HTML(html)
    tds = tree.xpath('//table[@id="Room1__room_map_"]/tr[position()>1]/td[position()>1]')
    tmp = []
    for i in tds:
        title = i.xpath('./@title')
        if title:
            style = i.xpath('./@style')[0]
            if background_color in style:
                house_info = title[0].split('\n')
                dict_tmp = {}
                for h in house_info:
                    info = h.split('：')
                    dict_tmp[info[0]] = info[1]
                tmp.append(dict_tmp)

    # print(tmp)
    # save_data(tmp)

    df = pd.DataFrame(tmp, columns=list(tmp[0].keys()))
    print(df)

    # print("down")


def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        print("pass")


def save_data(data):
    titles = list(data[0].keys())
    with open('房屋备案信息.csv', 'a+', encoding='utf_8_sig-', newline='') as f:
        f_csv = csv.DictWriter(f, titles)
        f_csv.writerows(data)


if __name__ == '__main__':
    main()
