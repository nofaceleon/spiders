import requests
from requests.exceptions import RequestException
import xlwt


# 爬取懂车帝所有汽车


def main():
    offset = 1
    limit = 30

    title = {
        "outter_name": "车名",
        "brand_name": "品牌名",
        "max_price": "最高价",
        "min_price": "最低价",
        "dealer_price": "价格描述"
    }

    title_keys = list(title.keys())

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')
    # 写入表头
    for i in range(len(title_keys)):
        # print(title[title_keys[i]])
        ws.write(0, i, title[title_keys[i]])
        # pass
    row = 1
    while 1:
        print(f"第{offset}页")
        params = {
            "offset": offset,
            "limit": limit,
            "is_refresh": 0,
            "city_name": "合肥"
        }
        base_url = "https://www.dongchedi.com/motor/pc/car/brand/get_select_series"
        data_json = get_url(base_url, params)
        for i in data_json['data']['series']:
            for k in title_keys:
                # print(f"row:{row}, col: {title_keys.index(k)}, v: {i[k]}")
                ws.write(row, title_keys.index(k), i[k])
            row += 1
        if not data_json['data']['series']:
            break
        offset += 1
    wb.save('./cars2.xls')
    print("爬取完毕")


def get_url(base_url, data):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    try:
        r = requests.post(base_url, data=data, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except RequestException:
        return None


if __name__ == '__main__':
    main()
