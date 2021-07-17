import pandas as pd
import requests
from requests.exceptions import RequestException


def main():
    html = get_html('http://www.chinamoney.com.cn/r/cms/www/chinamoney/data/currency/bk-lpr.json')
    data = get_content(html)
    df = pd.DataFrame(data)
    print(df)
    # res = sendMail.send_email('LRU利率', df.to_html())
    # print(res)
    # print(html['data']['showDateCN'])


def get_content(html):
    content = []
    data = {
        'date': html['data']['showDateCN'],
    }
    for i in html['records']:
        data[i['termCode']] = i['shibor'] + '%'
    content.append(data)
    return content


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            # r.encoding = 'utf-8'
            return r.json()
        else:
            return None
    except RequestException:
        return None


if __name__ == '__main__':
    main()
