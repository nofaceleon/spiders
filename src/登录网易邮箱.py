import time
import requests
from selenium.webdriver import Chrome


def main():
    web = Chrome()
    web.get('https://mail.163.com/')
    time.sleep(2)
    web.find_element_by_xpath('//input[id="auto-id-1623411551021"]').send_keys('songkindle')

    input()


if __name__ == '__main__':

    r = requests.get("http://ggjfwpt.luan.gov.cn/")
    if r.status_code != 200:
        print("cuowuo")
    else:
        print("success")

    # main()
