import time
from mako.template import Template
from spider import get_weekly, get_star_billboard


def run():
    """
    1. 下载抖音iDou榜单所有数据
    2. 按照https://github.com/Jannchie/Historical-ranking-data-visualization-based-on-d3.js构建数据用于可视化
        1. config.json
        2. data.csv
    3. 下载源码，替换config.json，导入data.csv
    4. 视频录制
    :return:
    """
    # 用户头像，写入config.json
    user_avatar = {}
    # 累计数据.csv，写入时按照，用户昵称重新排序
    star_total_data = {}
    # 每周数据.csv，写入时按照，用户昵称重新排序
    star_week_data = {}

    # 下载抖音iDou榜单，总共的周数
    billboard_weekly_list = get_weekly()
    # 下载每个榜单周期的数据
    billboard_weekly_list = reversed(billboard_weekly_list)
    for row in billboard_weekly_list:
        start_timestamp = row['start_time']
        end_timestamp = row['end_time']
        start_date = time.strftime("%Y.%m.%d", time.localtime(start_timestamp))
        end_date = time.strftime("%Y.%m.%d", time.localtime(end_timestamp))
        edition_no = row['edition_no']
        title = f"第{edition_no}期 {start_date} - {end_date}"
        billboard_data = get_star_billboard(row['uid'])
        user_list = billboard_data.get("user_list", [])
        for idx, user in enumerate(user_list):
            user_info = user['user_info']
            # 获取该明星此周的数据
            user_week_data_list = star_week_data.get(user_info['nickname'], [])
            top_times = user_week_data_list[-1]['top_times'] if user_week_data_list else 0
            if idx == 0:
                # 此周是top
                top_times += 1
            user_week_data_list.append(
                {
                    "name": user_info['nickname'],
                    "type": f"{top_times}周",
                    "top_times": top_times,
                    "value": user['hot_value'],
                    "date": title
                }
            )
            star_week_data[user_info['nickname']] = user_week_data_list
            # 获取明星的累计数据，取最后一周的数据进行累计
            user_total_data_list = star_total_data.get(user_info['nickname'], [])
            user_total_data_list.append(
                {
                    "name": user_info['nickname'],
                    "type": f"{top_times}周",
                    "value": user['hot_value'] + user_total_data_list[-1]['value'] if user_total_data_list else user[
                        'hot_value'],
                    "date": title}
            )
            star_total_data[user_info['nickname']] = user_total_data_list

            # 写入用户头像
            if user_info['nickname'] not in user_avatar:
                user_avatar[user_info['nickname']] = user_info['avatar_thumb']['url_list'][0]

    # 每周数据
    with open('every_weekly_data.csv', 'a', encoding='utf-8') as f:
        f.write("name,type,value,date\n")
        for users in star_week_data.values():
            for user in users:
                f.write(f"{user['name']},{user['type']},{user['value']},{user['date']}\n")

    # 累计数据
    with open('total_data.csv', 'a', encoding='utf-8') as f:
        f.write("name,type,value,date\n")
        for users in star_total_data.values():
            for user in users:
                f.write(f"{user['name']},{user['type']},{user['value']},{user['date']}\n")

    # 用户头像，写入config.json
    imgs = ['"{}": "{}"'.format(nickname, img_url) for nickname, img_url in user_avatar.items()]
    img_str = ",".join(imgs) if imgs else ""
    config_js_to_visualization = Template(filename='base_config.mako', input_encoding='utf-8')
    with open('config.js', 'a', encoding='utf-8') as f:
        f.write(config_js_to_visualization.render(img_str=img_str))


if __name__ == "__main__":
    run()
