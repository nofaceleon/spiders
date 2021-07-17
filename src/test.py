import re
# import sys, getopt
import requests

#
# strs = "nihao@#$%^&*|,.?"":[yes]world"
#
# res = re.sub("[@#^&%$*&\[\]]", "", strs)
# print(res)


# title = {
#     "outter_name": "车名",
#     "brand_name": "品牌名",
#     "max_price": "最高价",
#     "min_price": "最低价",
#     "dealer_price": "价格描述"
# }
#
# print(title)
#
# title['outter_name'] = 'hello world'
# print(title)
# title.pop('min_price')
# print(title)
#
# print("hello %s test %.2f" % ("world", 110))

# strsfs = 'http://www.baidu.com'
# flag = False
# for i in ['http2', 'www2', 'badu']:
#     if i in strsfs:
#         flag = True
#
# print(flag)

# with open('./files/.env', encoding='utf-8') as f:
#     info = f.read()
#
# print(info)
#
# db_type = re.compile('^TYPE = (.*?)', re.S)
# print(re.findall(db_type, info))

# args = sys.argv
#
# html = """
#         <img src="https://oss1.wandougongzhu.cn/ab0daab1cd440792c50941fedb0b6ced.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss4.wandougongzhu.cn/cf7c3066743855e52f94d346e0c60c9c.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss3.wandougongzhu.cn/871ee29fe69595bf4e4b8ca81a1722af.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss1.wandougongzhu.cn/92f7f902618a2cd58cc0faa87874aa33.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss4.wandougongzhu.cn/b11c5c9cc8ac23467ea707ae4a917a3d.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss5.wandougongzhu.cn/88b2631842d8f3f06399eb67e4a94241.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss2.wandougongzhu.cn/45286d49fd63ec8791db23f625df8311.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss4.wandougongzhu.cn/8869cecf36489365efed939785ab642d.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss5.wandougongzhu.cn/2c5b81e807caa40f839f696f48fe4a4c.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss3.wandougongzhu.cn/d85a82dea0694badea7f16320b999b4d.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss1.wandougongzhu.cn/3babe90544a64128d968b3b2f08737df.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# 		<img src="https://oss2.wandougongzhu.cn/560e626d4e4f50e7b5c43992c3aee230.png?x-oss-process=image/resize,w_1242,h_4000/format,webp" alt="商品详情">
# """
#
# html2 = """
# https://oss2.wandougongzhu.cn/49168ae67afbb58ee35f2b3afbaa6310.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss4.wandougongzhu.cn/dff2a60c9ed837e4078d0a96167a2dd6.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss4.wandougongzhu.cn/dd245a884aaf90744b63c714c2bcc427.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss1.wandougongzhu.cn/2f46be23e6b6fc7524be4c73afdae82e.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss4.wandougongzhu.cn/190e0b0b4517b5927609007740ecfedd.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss1.wandougongzhu.cn/8ffafcbc29023e2284706b9f3edcb5f1.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss3.wandougongzhu.cn/2642443dd4ee10d5f88ff7700ae72d2f.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss1.wandougongzhu.cn/315562357ee4cb386b897a418ccc8e6b.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss4.wandougongzhu.cn/b9ec9182d496f58b17ead6e3a1399cb9.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss3.wandougongzhu.cn/47a07701a8435fa3a4d9594fdb85f6b5.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# https://oss5.wandougongzhu.cn/e980eba15ed96254cf444c47b8cbc51f.png?x-oss-process=image/resize,w_1242,h_4000/format,webp
# """
#
#
#
#
# r = requests.get("https://h5.wandougongzhu.cn/product/10078.html?house_id=0&act_id=0&loc=list%3Ag%3A0%3A426%3A%3A0%3Ageneral%3Ag_10078&ll=list%3A0&lr=g_10078")
#
# print(r.text)
# exit()
#
#
#
#
# imgs = re.findall('<img src="(.*?)\?.*?,webp\n" alt="商品详情">', html)
# imgs2 = re.findall(r'(.*?)\?.*?,webp', html2)
#
# print(imgs2)
# exit()
#
# index = 1
# for i in imgs:
#     r = requests.get(i)
#     if r.status_code == 200:
#         with open(f'./files/{index}.png', 'wb') as f:
#             f.write(r.content)
#         print(f"down--{index}")
#         index += 1
#     else:
#         print("fail")


"""
function nscaler(a) {
    var b = "";
    var ar = String(a).split('');
    $.each(ar, function (i, e) {
        switch (e) {
        case "0":
            b += "0";
            break;
        case "1":
            b += "2";
            break;
        case "2":
            b += "5";
            break;
        case "3":
            b += "8";
            break;
        case "4":
            b += "6";
            break;
        case "5":
            b += "1";
            break;
        case "6":
            b += "3";
            break;
        case "7":
            b += "4";
            break;
        case "8":
            b += "9";
            break;
        case "9":
            b += "7";
            break
        }
    });
    return b
}
"""


def jiami():
    b = ''
    tmp = "6124156"
    ls = list(tmp)
    replaces = {
        '0': '0',
        '1': '2',
        '2': '5',
        '3': '8',
        '4': '6',
        '5': '1',
        '6': '3',
        '7': '4',
        '8': '9',
        '9': '7',
    }
    res = ''.join([replaces[i] for i in ls])
    print(res)

    # print(list(tmp))


if __name__ == '__main__':
    jiami()
    # strs = '3.123213 m'
    # # num = re.search(r'\d\.\d+|\d+', strs).group()
    # num = re.search(r'\d+(\.\d+)?', strs).group()
    # print(num)
