import requests
import re


def main():
    html = get_html("http://wanyouw.com/")
    key = get_post_key(html)
    print(key)

    hot_list = ["weibo_topsearch", "weixin_news", "bilibili_topsearch", "lssdjt_topsearch"]

    for i in hot_list:
        print(i)
        hot_data = get_hot_data(i, key)
        print(hot_data)
        print("===============")


def get_html(url, method="GET", data="", response_type="text"):
    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://wanyouw.com',
        'Referer': 'http://wanyouw.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'PHPSESSID=p0o9a1mmbrcjg4ogmrmj428v4b'
    }

    r = requests.request(method, url, headers=headers, data=data)
    if r.status_code == 200:
        if response_type == 'text':
            return r.text
        elif response_type == 'json':
            return r.json()
        else:
            print("参数错误")
    else:
        print(r.status_code)


def get_post_key(html):
    key = re.compile(r'{ type: _type ,key:"(.*?)" }')
    data = re.findall(key, html)
    if data:
        return data[0]
    else:
        return ""


def get_hot_data(hot_type, post_key):
    payload = f"type={hot_type}&key={post_key}"
    data = get_html("http://apiv2.iotheme.cn/hot/get.php", "POST", payload, "json")
    return data


if __name__ == '__main__':
    main()
