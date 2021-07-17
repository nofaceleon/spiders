import requests
from requests.exceptions import RequestException


def main():
    key = str(input("请输入搜索的图书:"))
    if not key:
        print("关键字不能为空")
    else:
        base_url = f"https://search.douban.com/book/subject_search?search_text={key}&cat=1001"
        html = get_html(base_url)
        print(html)


def get_html(base_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 ",
    }
    try:
        r = requests.get(base_url, headers=headers)
        if r.status_code == 200:
            return r.text
        else:
            print(f"请求失败,状态码:{r.status_code}")
    except RequestException:
        print("请求异常")
        exit()


if __name__ == '__main__':
    main()
