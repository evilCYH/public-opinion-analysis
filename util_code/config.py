host_ip = "127.0.0.1"  # 你的mysql服务器地址
host_user = "root"
password = "123456"  # 你的mysql密码
db = 'yuqing'
port = 3306
charset= 'utf8mb4'

# 配置需要采集的内容 'news','tieba','weibo'
spider_list = ['weibo']

weibo_config = {
    "user_id": "1891849065",  # 修改
    "filter": 1,
    "cookie": "__guid=52195957.4453683298486628000.1609668843467.1792; _T_WM=47333895929; WEIBOCN_FROM=1110003030; SCF=AnXIT83Si_hu1XPUg0xkcd71WChIclQvMGkuu9CVpYSoP_zsNBXyYqs0SfP1k3vlIaFn5dFcpKu6BLDoYAEoj1k.; SUB=_2A25NNbw_DeRhGeVJ7FMU8i3FzjyIHXVu2cR3rDV6PUJbktANLVLjkW1NT836rVaTbwBK3C5_n9p9njSjHz-Z0yv3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF58sQ7hpaDVH.VKmpUXiQN5JpX5K-hUgL.FoeNS02feoe4SK52dJLoIXnLxKMLB.zLB-BLxK-L1hqL1K.LxK-LBo2L1--LxKBLB.2L12-LxKqL1hnL1K2LxKML1-2L1hBLxKqL1-eLB-2LxKqL1-BLBK-t; SSOLoginState=1613876335; ALF=1616468335; MLOGIN=1; XSRF-TOKEN=9b5d81; monitor_count=2; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076035889219623%26fid%3D1076033221547054%26uicode%3D10000011",
    "mysql_config": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "charset": "utf8mb4",
        "db":"yuqing"
    }
}