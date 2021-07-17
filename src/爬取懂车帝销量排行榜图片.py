import requests
from requests.exceptions import RequestException
import os


def main():
    offset = 0
    limit = 50
    flag = True
    while flag:
        print(offset)
        base_url = f"https://www.dongchedi.com/motor/car_show/v1/get_sells_rank/?month=202104&rank_type=100&limit={limit}&city_name=%E5%90%88%E8%82%A5&offset={offset} "
        data_json = get_url(base_url)
        path = "../懂车帝"
        if not os.path.exists(path):
            os.mkdir(path)
        for i in data_json['data']['list']:
            file_name = f"{path}/{i['rank']}-{i['series_name']}.png"
            with open(file_name, 'wb') as f:
                f.write(requests.get(i['image']).content)
                f.close()
        offset += limit
        if not data_json['data']['paging']['has_more']:
            break
    print("爬取完毕")


def get_url(base_url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    try:
        r = requests.get(base_url, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except RequestException:
        return None


if __name__ == '__main__':
    main()
