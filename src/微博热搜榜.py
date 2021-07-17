import requests
from lxml import etree


def main():
    html = get_html("https://s.weibo.com/top/summary?Refer=top_hot")
    tree = etree.HTML(html)
    tds = tree.xpath('//td[@class="td-02"]')
    buffer = []
    for i in tds:
        buffer.append({
            "title": i.xpath('./a/text()')[0],
            "link": "https://s.weibo.com/" + i.xpath('./a/@href')[0].lstrip('/')
        })

    print(buffer)


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        print(r.status_code)


if __name__ == '__main__':
    main()
