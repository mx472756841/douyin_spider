import requests


def get_weekly():
    """
    通过抓包工具，获取明星势力榜的所有统计周期
    :return:
    """
    billboard_weekly_list = []
    url = "https://api3-normal-c-lf.amemv.com/aweme/v1/hotsearch/branch_billboard/weekly/list/"
    result = requests.get(url)
    if result.status_code == 200:
        data = result.json()
        if data.get('status_code') == 0:
            billboard_weekly_list = data.get('billboard_weekly_list', [])
    return billboard_weekly_list


def get_star_billboard(edition_uid):
    """

    :param edition_uid: weekly id 通过接口获取
    :return:
    """
    url = f"https://api3-normal-c-lf.amemv.com/aweme/v1/hotsearch/star/billboard/?type=1&edition_uid={edition_uid}"
    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    else:
        return {}
