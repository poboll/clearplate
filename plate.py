# 光盘行动打卡 API
import requests
from datetime import datetime
import time

# 打卡光盘
def daka(token):
    headers = {
        'Host': 'api.clearplate.org.cn',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-app-platform': 'wx',
        'x-form-id-list': '[]',
        'x-token': token,
        'x-version': '6.0.0',
        'accept-language': 'zh-cn',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001026) NetType/WIFI Language/zh_CN',
        'referer': 'https://servicewechat.com/wx6a4976bd627fc4ca/428/page-frame.html',
        'x-oauth-type': '1',
        'x-access-token': 'lI8DB7FI1F3ovLdg3HMSInak62o9XESY',
    }

    params = (
        ('r', 'user-clear-plate/clear-plate'),
    )

    data = 'path_url=%2FclockImg%2F2021%2F11%2F14%2Fe8CmfsNHSA3ys6ZNsPWQTSyMwzfc3wMX1636862639397.jpg&group_id=1282&location=23.308025224%2C113.563811329'

    response = requests.post('https://api.clearplate.org.cn/index.php', headers=headers, params=params, data=data)
    return response
# 领取小光奖励
def lingqu(token):
    headers = {
        'Host': 'api.clearplate.org.cn',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-app-platform': 'wx',
        'x-form-id-list': '[]',
        'x-token': token,
        'x-version': '6.0.0',
        'accept-language': 'zh-cn',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
        'referer': 'https://servicewechat.com/wx6a4976bd627fc4ca/428/page-frame.html',
        'x-oauth-type': '1',
        'x-access-token': 'lI8DB7FI1F3ovLdg3HMSInak62o9XESY',
    }

    params = (
        ('r', 'food-users/harvest'),
    )

    data = 'food_id=2'

    response = requests.post('https://api.clearplate.org.cn/index.php', headers=headers, params=params, data=data)
    return response

# 喂小光
def feed(token):
    headers = {
        'Host': 'api.clearplate.org.cn',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-app-platform': 'wx',
        'x-form-id-list': '[]',
        'x-token': token,
        'x-version': '6.0.0',
        'accept-language': 'zh-cn',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
        'referer': 'https://servicewechat.com/wx6a4976bd627fc4ca/428/page-frame.html',
        'x-oauth-type': '1',
        'x-access-token': 'lI8DB7FI1F3ovLdg3HMSInak62o9XESY',
    }

    params = (
        ('r', 'food-users/food-user-eat'),
    )

    data = 'food_id=2'

    response = requests.post('https://api.clearplate.org.cn/index.php', headers=headers, params=params, data=data)
    return response

# 领取红包
def hongbao(token):
    headers = {
        'Host': 'api.clearplate.org.cn',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-app-platform': 'wx',
        'x-form-id-list': '[]',
        'x-token': token,
        'x-version': '6.0.0',
        'accept-language': 'zh-cn',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
        'referer': 'https://servicewechat.com/wx6a4976bd627fc4ca/428/page-frame.html',
        'x-oauth-type': '1',
        'x-access-token': 'lI8DB7FI1F3ovLdg3HMSInak62o9XESY',
    }

    params = (
        ('r', 'advertisement-list/user-advertisement'),
    )

    data = 'advertisement_id=1'

    response = requests.post('https://api.clearplate.org.cn/index.php', headers=headers, params=params, data=data)
    return response

def nengliang(token):
    headers = {
        'Host': 'api.clearplate.org.cn',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-app-platform': 'wx',
        'x-form-id-list': '[]',
        'x-token': token,
        'x-version': '6.0.0',
        'accept-language': 'zh-cn',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
        'referer': 'https://servicewechat.com/wx6a4976bd627fc4ca/428/page-frame.html',
        'x-oauth-type': '1',
        'x-access-token': 'lI8DB7FI1F3ovLdg3HMSInak62o9XESY',
    }

    params = (
        ('r', 'food-users/get-energy'),
    )

    response = requests.post('https://api.clearplate.org.cn/index.php', headers=headers, params=params)
    return response

#data = daka('a5b4a35bd2550e902efb06f32be3b491ffda1786')
#print(data.text)
# 每n秒执行一次
def timer(n,tokens):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data = daka(token)
        print(data.text)
        data = feed(token)
        print(data.text)
        data = lingqu(token)
        print(data.text)
        data = hongbao(token)
        print(data.text)
        data = nengliang(token)
        print(data.text)        
        time.sleep(n)
# 3600*2
token = '0219f2e2a4ef7e5da21efe8ed34e2d6e41197c38'
timer(600,token)

