import bs4
import datetime
import execjs
import os
import requests

# 微信推送
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

# 获取 GitHub Secrets 中的参数
user_id = os.environ["STUDENT_ID"]  # 学号
user_passwd = os.environ["PASSWORD"]  # 密码
user_name = os.environ["NAME"]  # 姓名
user_school = os.environ["SCHOOL"]  # 学院
user_major = os.environ["MAJOR"]  # 专业
user_type = os.environ["TYPE"]  # 类型
user_phone = os.environ["PHONE"]  # 手机号
user_master = os.environ["MASTER"]  # 班主任
user_building = os.environ["BUILDING"]  # 宿舍楼
user_room = os.environ["ROOM"]  # 宿舍号
app_id = os.environ["APP_ID"]  # 微信推送 app_id
if_wepush = os.environ["IF_WEPUSH"]  # 是否启用微信推送

# 报平安成功的时间
report_time = datetime.datetime.now().strftime("%Y-%m-%d")


# 主逻辑
def report():
    # 接口地址
    login_url = 'http://cas.bjfu.edu.cn/cas/login'
    with requests.session() as s:
        page = s.get(login_url).text
        rsa_js = requests.get('http://cas.bjfu.edu.cn/cas/comm/js/des.js').text
        # 获取返回的页面
        soup = bs4.BeautifulSoup(page, 'html.parser')
        lt = soup.find('input', id='lt')['value']
        execution = soup.find('input', attrs={'name': 'execution'})['value']

        key = user_id + user_passwd + lt
        rsa = execjs.compile(rsa_js).call('strEnc', key, '1', '2', '3')
        # 组织参数列表
        data = {
            'rsa': rsa,  # 加密后的账号密码
            'ul': str(len(user_id)),  # 用户名长度
            'pl': str(len(user_passwd)),  # 密码长度
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit'
        }
        # 登录
        s.post(login_url, data=data)
        # 完成智慧北林登录授权

        token_url = 'https://x.bjfu.edu.cn/tp_up/getToken'
        report_url = 'https://x.bjfu.edu.cn/tp_up/question/question/add'
        s.get('https://x.bjfu.edu.cn/tp_up/view?m=bjfu#act=question/question')
        token1 = s.post(token_url).text
        report_header = {
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Origin': 'https://x.bjfu.edu.cn',
            'Referer': 'https://x.bjfu.edu.cn/tp_up/view?m=bjfu',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
            'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'sec-ch-ua-platform': '"Windows"'
        }
        report_data1 = {
            "mapping": "add2",
            "token": token1,
            "key": "PK_ID",
            "XM1": user_name,
            "XH1": user_id,
            "SZXY1": user_school,
            "SZBJ1": user_major,
            "XSLX": user_type,
            "FDY1": user_master,
            "DSXM1": "",
            "GKSYD_TEXT": "请选择",
            "GKSYD": "",
            "SJH": user_phone,
            "SZLY": user_building,
            "SZSS": user_room,
            "SQCS": "0",
            "JRRQ": report_time,
            "JRSTZK_TEXT": "良好",
            "JRSTZK": "1",
            "ZLQK": "",
            "JTCYJKZK_TEXT": "良好(Well)",
            "JTCYJKZK": "1",
            "MQSFZJ_TEXT": "京内(in Beijing)",
            "MQSFZJ": "京内",
            "MQSZS_TEXT": "请选择",
            "MQSZS": "",
            "MQSZSX": "",
            "MQSZQX": "",
            "SFJHFJ_TEXT": "否(No)",
            "SFJHFJ": "否",
            "JHFJRQ": "",
            "JHFJJT_TEXT": "请选择",
            "JHFJJT": "",
            "JHFJCC": "",
            "JTSFDX_TEXT": "是(Yes)",
            "JTSFDX": "是",
            "ZJJTZZ": "",
            "JSRS_TEXT": "请选择",
            "JSRS": "",
            "JSSFLJ_TEXT": "请选择",
            "JSSFLJ": "",
            "JSFJQSZS_TEXT": "请选择",
            "JSFJQSZS": "",
            "JSFJQXXZZ": "",
            "JSFJRQ": "",
            "JSFJYY": "",
            "JSFJJTGJ_TEXT": "请选择",
            "JSFJJTGJ": "",
            "JSFJCCHB": "",
            "HJQJSFLJ_TEXT": "否(No)",
            "HJQJSFLJ": "否",
            "FJQSZS_TEXT": "请选择",
            "FJQSZS": "",
            "FJQSZSX": "",
            "FJRQ": "",
            "FJJTGJ_TEXT": "请选择",
            "FJJTGJ": "",
            "FJCC": "",
            "FJYY": "",
            "MQSZG": "",
            "DA1": "否(No)",
            "DA2": "否(No)",
            "SFGL": "否",
            "GLYY": "",
            "GLDD": "",
            "TW1_TEXT": "36.0℃及以下",
            "TW1": "36.0",
            "TW2_TEXT": "36.0℃及以下",
            "TW2": "36.0",
            "TW3_TEXT": "36.0℃及以下",
            "TW3": "36.0",
            "JSXM1": "",
            "JSDW1": "",
            "JSQX1": "",
            "JSXM2": "",
            "JSDW2": "",
            "JSQX2": "",
            "JSXM3": "",
            "JSDW3": "",
            "JSQX3": "",
            "JSXM4": "",
            "JSDW4": "",
            "JSQX4": "",
            "JSXM5": "",
            "JSDW5": "",
            "JSQX5": "",
            "JSXM6": "",
            "JSDW6": "",
            "JSQX6": ""
        }
        code1 = s.post(report_url, headers=report_header, json=report_data1)
        token2 = s.post(token_url).text
        report_data2 = {
            'id_number': user_id,
            'mapping': 'messageSend',
            'token': token2
        }
        code2 = s.post(report_url, headers=report_header, json=report_data2)
        if code1.text != 'true':
            return -1
        elif code2.text != 'true':
            return -2
        else:
            return 0


def send_message(status_t):
    app_secret = os.environ["APP_SECRET"]  # 微信推送 app_secret
    template_id = os.environ["TEMPLATE_ID"]  # 微信推送 template_id
    # 启用微信推送
    if app_id:
        client = WeChatClient(app_id, app_secret)
        wm = WeChatMessage(client)
        if status_t == -1:
            data = {
                "status": user_id + "报平安失败！",
            }
            res = wm.send_template(user_id, template_id, data)
        elif status_t == -2:
            data = {
                "status": user_id + "已报平安，微信通知失败！",
            }
            res = wm.send_template(user_id, template_id, data)
        else:
            data = {
                "status": user_id + "报平安成功！",
            }
            res = wm.send_template(user_id, template_id, data)


if __name__ == '__main__':
    status = report()
    if if_wepush == 1:
        send_message(status)
    if status == -1:
        print('报平安脚本：\n报平安失败！')
    elif status == -2:
        print('报平安脚本：\n已报平安，微信通知失败！')


