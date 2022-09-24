# 腾讯云执行脚本，如不需要可忽略
import requests


def run():
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'token 你的TOKEN',
    }

    data = '{"event_type": "autoReportPeace"}'

    response = requests.post(f'https://api.github.com/repos/你的用户名/reportPeace/dispatches',
                             headers=headers, data=data)


# 云函数入口
def main_handler(event, context):
    return run()