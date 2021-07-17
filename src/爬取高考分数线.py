import requests
import csv
import os


def main():
    filename = '../files/高考分数线.csv'
    urls = get_urls()
    for i in urls.values():
        is_writer_header = False if os.path.exists(filename) else True
        print(i)
        content = get_content(i)
        content = handle_content(content)
        if content:
            save_data(content, filename, is_writer_header)
    print("done")


def get_province():
    province = {
        11: "北京",
        12: "天津",
        13: "河北",
        14: "山西",
        15: "内蒙古",
        21: "辽宁",
        22: "吉林",
        23: "黑龙江",
        31: "上海",
        32: "江苏",
        33: "浙江",
        34: "安徽",
        35: "福建",
        36: "江西",
        37: "山东",
        41: "河南",
        42: "湖北",
        43: "湖南",
        44: "广东",
        45: "广西",
        46: "海南",
        50: "重庆",
        51: "四川",
        52: "贵州",
        53: "云南",
        54: "西藏",
        61: "陕西",
        62: "甘肃",
        63: "青海",
        64: "宁夏",
        65: "新疆",
        71: "香港",
        81: "澳门",
        82: "台湾",
        99: "其它",
        100: "不分省",
        0: "其它"
    }
    return province


def get_urls():
    urls = {}
    province = get_province()
    for province_id, province_name in province.items():
        base_url = f"https://static-data.eol.cn/www/2.0/proprovince2021/{province_id}/pro.json"
        urls[province_name] = base_url

    return urls


def get_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"状态{r.status_code}")


# 处理每个省份的分数信息
def handle_content(data):
    tmp = []
    try:
        all_data = data['data']
        # print(type(all_data))
        # exit()
        tmp = []
        for year, value in all_data.items():
            for k, v in value.items():
                tmp += v
    except:
        print("数据异常")

    return tmp


def save_data(data, filename, is_writer_header):
    titles = data[0].keys()
    with open(filename, 'a+', encoding='utf_8_sig', newline='') as f:
        f_csv = csv.DictWriter(f, titles)
        if is_writer_header:
            f_csv.writeheader()  # 写入表头
        f_csv.writerows(data)


if __name__ == '__main__':
    main()
