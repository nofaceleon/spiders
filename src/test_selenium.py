import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def main(key):
    # 无头浏览器
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')

    web = Chrome(options=opt)
    web.get("https://movie.douban.com/")
    web.find_element_by_xpath('//input[@id="inp-query"]').send_keys(key, Keys.ENTER)
    all_list = []
    for i in range(1):
        els = web.find_elements_by_xpath('//div[@class="detail"]/div[@class="title"]')
        for e in els:
            all_list.append(e.text)
        # 点击下一页
        # web.find_element_by_xpath('//a[@class="next"]').click()
        # time.sleep(1)

    with open('../files/豆瓣搜索页2.txt', 'w+', encoding='utf-8') as f:
        for i in all_list:
            f.write(i + '\n')
    print("down")


if __name__ == '__main__':
    key = input('输入关键字: ')
    main(key)
