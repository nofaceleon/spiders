import requests
import datetime


def main_handler(event, context):
    url = "https://api.live.bilibili.com/sign/doSign"

    payload = {}
    headers = {
        'Cookie': '_uuid=0AFDC3F2-C9BF-C0CB-1197-5C7D9FEDA7DA51592infoc; '
                  'buvid3=83B984DE-AEC4-4A94-9D30-17BAEFCB991A18538infoc; CURRENT_FNVAL=80; blackside_state=1; '
                  'rpdid=|(J|)|))lll~0J\'uYukY)mlYJ; fingerprint=5866a9af78b8810d07007b2779f6d399; '
                  'buvid_fp=83B984DE-AEC4-4A94-9D30-17BAEFCB991A18538infoc; '
                  'buvid_fp_plain=BDA95AC1-BBC8-463E-B82B-E9B11F95B951155832infoc; '
                  'SESSDATA=da7237fe%2C1628241594%2Cfdb38%2A21; bili_jct=0c0965b67d3363fd94416b78107d1fb7; '
                  'DedeUserID=244113962; DedeUserID__ckMd5=5029efc737d19daa; sid=m3eookht; '
                  'LIVE_BUVID=AUTO1016126907444365; bp_article_offset_244113962=523563058920772735; '
                  'CURRENT_QUALITY=80; bp_video_offset_244113962=530039195286944604; '
                  'bp_t_offset_244113962=530534714254165360; PVID=4; bsource=search_baidu '
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    send_email(response.text)


def send_email(data):
    pass


main_handler(1, 1)
