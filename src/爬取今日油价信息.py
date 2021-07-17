# -*- coding: utf-8 -*-
import datetime
import smtplib
from email.mime.text import MIMEText
import requests
from requests.exceptions import RequestException
from lxml import etree
import xlwt
import pandas as pd
from sqlalchemy import create_engine


def main():
    url = "http://youjia.chemcp.com/"
    html = get_html(url)
    data = get_content(html)
    df = pd.DataFrame(data)
    print(df)
    # save_data_to_mysql(data)
    # format_html = new_format_data(data)
    # print(format_html)
    # send_email(format_data)

    # send_email(format_data(data))
    # exit()
    # dataa = ['|'.join(i) for i in data]
    # strs = ''
    # for i in dataa:
    #     strs += i + '\n'
    # strs = ['\n'.join(i) for i in dataa]
    # print(strs)
    # send_email(strs)
    # save_data(data)
    # print("done")


def get_content(html):
    tree = etree.HTML(html)
    all_list = tree.xpath('//*[@id="box"]/div[1]/div[1]/div[2]/table/tr/td/*/text()'
                          ' | //*[@id="box"]/div[1]/div[1]/div[2]/table/tr/td/text()')
    tmp = []
    for i in range(0, len(all_list), 7):
        tmp.append(all_list[i:i + 7])
    # lists = tree.xpath('//*[@id="box"]/div[2]/table/tr[2]/td/a/text()')
    # print(title + lists)
    return tmp


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'gbk'
            return r.text
        else:
            return None
    except RequestException:
        return None


def save_data(data):
    today = datetime.date.today()
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')
    row = 0
    for i in data:
        for v in i:
            ws.write(row, i.index(v), v)
        row += 1
    wb.save(f"./今日油价{today}.xls")


def send_email(data):
    pass


def format_data(data):
    content = ''
    for i in data:
        table_str = "<tr>"
        for k in i:
            table_str += f"<td>{k}</td>"
        table_str += "</tr>"
        content += table_str
    html = f'<table border = "1" style="border-collapse: collapse;">{content}</table>'
    return html


def new_format_data(data):
    df = pd.DataFrame(data[1:], columns=data[:1][0])
    return df.to_html()


def save_data_to_mysql(data):
    df = pd.DataFrame(data[1:], columns=['area', '89#', '92#', '95#', '98#', '0#', 'update_time'])
    # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/manage')
    df.to_sql('oil_price', con=engine, if_exists='replace')


if __name__ == '__main__':
    main()
