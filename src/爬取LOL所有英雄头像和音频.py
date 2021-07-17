import datetime
import requests
import os
from requests.exceptions import RequestException

url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.212 Safari/537.36 "
}


def main():
    # 图片保存路径
    img_path = "./img/"
    # 音频保存路径
    ogg_path = "./ogg/"
    data_json = get_url(url)
    for i in data_json["hero"]:
        img_url = "https://game.gtimg.cn/images/lol/act/img/champion/" + i["alias"] + ".png"
        img_file_name = img_path + i["name"] + ".png"
        download(img_url, img_file_name)

        ogg_url = i["banAudio"]
        ogg_name = ogg_path + i["name"] + ".ogg"
        download(ogg_url, ogg_name)


# 获取数据
def get_url(base_url):
    try:
        r = requests.get(base_url, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except RequestException:
        return None


# 下载图片
# def get_img(img_url, img_file_name):
#     chek_path(img_file_name)
#     with open(img_file_name, "wb") as img:
#         img.write(requests.get(img_url).content)
#         img.close()
#
#
# # 下载音频
# def get_ogg(ogg_url, ogg_name):
#     chek_path(ogg_name)
#     with open(ogg_name, "wb") as ogg:
#         ogg.write(requests.get(ogg_url).content)
#         ogg.close()

# 下载资源
def download(source_url, name):
    chek_path(name)
    with open(name, "wb") as f:
        f.write(requests.get(source_url).content)
        f.close()


# 创建目录
def chek_path(file_name):
    path = os.path.dirname(file_name)
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':
    start = datetime.datetime.now()
    print("开始爬取")
    main()
    end = datetime.datetime.now()
    print("爬取完成,总耗时" + str((end - start).seconds) + "秒")
