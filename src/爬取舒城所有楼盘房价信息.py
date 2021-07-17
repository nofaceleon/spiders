import re
import time
import requests
import csv
from lxml import etree
import os

base_url = "http://www.ahscfdc.com/"
path = '../files'
filename = path + '/舒城所有楼盘价格信息.csv'


def main():
    start = time.time()
    check_path(path)
    building_info = get_all_building_info()
    # building_info = [['dfd',
    #                   'http://www.ahscfdc.com/ShowSection.aspx?Section=V1ooS8N%2fhIdX80Un1IhnTh0gX%2fHWeWZpnPnKkxCBXZhdOlVTyecU4A%3d%3d']]
    for i in building_info:
        # print(i[0])
        license_info = get_license_key(i[1])
        if not license_info:
            print(f"{i[0]}没有楼盘信息,跳过")
            continue
        # print(license_info)
        for t in license_info:
            data = get_building_detail(t, i[0])
            save_data(data, i[0])
    end = time.time()
    print(f'所有数据获取完毕总耗时{end - start}')


def get_house_status_info(key):
    house_status = {
        '#F0FFB6': '可售',
        '#FFFF66': '预定',
        '#82B4FF': '签约',
        '#96E686': '备案',
        '#E5E5E5': '自留',
        '#FFCCFF': '回迁',
        '#CC3399': '抵押',
        'Salmon': '政府回购',
        '#FF0000': '查封',
        '#6666CC': '限制',
        '#7030A0': '处理',
        '#FF8D00': '不可售',
        '#CFE1E9': '历史遗留',
        '#646464': '其他',
    }

    return house_status.get(key, '未知状态')


# 获取所有楼盘信息
def get_all_building_info():
    url = "http://www.ahscfdc.com/ShowBuild.aspx"
    html = get_html(url)
    tree = etree.HTML(html)
    tds = tree.xpath('//table[@id="ctl00_ContentPlaceHolder1_tbShowList"]/tr/td[@align="left"]/table/tr/td')
    tmp = []
    for td in tds:
        link = td.xpath('./a/@href')
        name = td.xpath('./a/text()')
        buffer = []
        if link:
            buffer.append(name[0])
            buffer.append(base_url + link[0])
            tmp.append(buffer)

            # print(html)
    # print(tmp)
    # exit()
    return tmp
    # print(tmp)


def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        print(f"status_code={r.status_code}")


# 获取许可证号
def get_license_key(url):
    html = get_html(url)
    tree = etree.HTML(html)
    links = tree.xpath('//table/tr/td[@class="border3"]/table[2]/tr/td/table/tr/td/a')
    tmp = []
    for i in links:
        link = i.xpath('./@href')
        if link and i.tail:
            # building_num = re.search(r'\d+', str(i.tail)).group()
            tmp.append(base_url + link[0])
            # print(building_num)
            # print(base_url + link[0])

        # 获取楼盘详情
    return tmp


def get_building_detail(url, building_name):
    html = get_html(url)
    tree = etree.HTML(html)
    tds = tree.xpath('//table[@id="Room1__room_map_"]/tr[position()>1]/td[position()>1]')
    building_detail = tree.xpath('//span[@id="lbTitle"]/text()')[0]
    building_id = re.search(r'[A-Za-z]*\d+', building_detail)
    if building_id:
        building_id = building_id.group()
    else:
        building_id = '0'
    tmp = []
    for i in tds:
        title = i.xpath('./@title')
        if title:
            style = i.xpath('./@style')[0]  # 房屋预售状态
            background_color = re.findall(re.compile(r'background-color:(.*?);'), style)[0]  # 提取背景色
            house_info = title[0].split('\n')
            dict_tmp = {
                '楼盘名称': building_name,
                '楼盘详细': building_detail,
                '幢': building_id,
                '楼层': i.xpath('../td[1]/text()')[0],
                '状态': get_house_status_info(background_color)
            }
            for h in house_info:
                info = h.split('：')
                value = info[1]
                if info[0] in ['套内面积', '建筑面积', '层高', '物价局备案价格']:
                    value = re.search(r'\d+(\.\d+)?', info[1])
                    if value:
                        value = value.group()
                    else:
                        value = '0'
                dict_tmp[info[0]] = value
            tmp.append(dict_tmp)
    return tmp


# 保存楼盘信息
def save_data(data, name):
    flag = True
    if os.path.exists(filename):
        flag = False
    # if not os.path.exists(filename):
    #     with open(filename, 'a+', encoding='utf_8_sig') as f:
    #         f.write(','.join(get_csv_title()) + '\n')
    titles = list(data[0].keys())
    with open(filename, 'a+', encoding='utf_8_sig', newline='') as f:
        # f_csv = csv.DictWriter(f, get_csv_title())
        f_csv = csv.DictWriter(f, titles)
        if flag:
            f_csv.writeheader()
        f_csv.writerows(data)
    print(f"{name}--保存完毕")


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


# def get_csv_title():
#     title = [
#         '楼盘名称',
#         '楼盘详细',
#         '幢',
#         '楼层',
#         '状态',
#         '室号',
#         '户型',
#         '套内面积',
#         '建筑面积',
#         '设计用途',
#         '层高',
#         '物价局备案价格'
#     ]
#
#     return title


if __name__ == '__main__':
    main()
