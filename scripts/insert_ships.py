import os
import django
from datetime import datetime
import random
import sys

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ship_track.settings')
django.setup()

from backend.models import ShipInfo  # 修改为您的 app 名称和模型路径

# 数据列表，按图示生成
ship_data = [
    {
        "ship_id": "BAHL",
        "ship_name": "连通",
        "ship_country": "中国",
        "ship_size": 120.5,
        "ship_model": "Product Carrier",
        "ship_weight": 20000.0,
        "ship_build_date": "2010-01-01",
        "ship_serve_date": "2011-01-01",
        "ship_status": 2,  # 航行
        "ship_longitude": round(random.uniform(120.0, 122.0), 6),
        "ship_latitude": round(random.uniform(30.0, 32.0), 6),
        "ship_text": "这是船舶连通的描述信息。",
    },
    {
        "ship_id": "BAKS",
        "ship_name": "信风广州",
        "ship_country": "中国",
        "ship_size": 140.8,
        "ship_model": "集装箱船",
        "ship_weight": 25000.0,
        "ship_build_date": "2012-05-15",
        "ship_serve_date": "2013-06-20",
        "ship_status": 1,  # 到港
        "ship_longitude": round(random.uniform(112.0, 114.0), 6),
        "ship_latitude": round(random.uniform(22.0, 24.0), 6),
        "ship_text": "信风广州是一艘现代化的集装箱船。",
    },
    {
        "ship_id": "BFEO",
        "ship_name": "国电6",
        "ship_country": "中国",
        "ship_size": 130.2,
        "ship_model": "散货船",
        "ship_weight": 22000.0,
        "ship_build_date": "2015-07-10",
        "ship_serve_date": "2016-08-05",
        "ship_status": 1,  # 到港
        "ship_longitude": round(random.uniform(110.0, 112.0), 6),
        "ship_latitude": round(random.uniform(22.0, 23.5), 6),
        "ship_text": "国电6是一艘散货船，负责煤炭运输。",
    },
    {
        "ship_id": "BHBO",
        "ship_name": "嘉航兴",
        "ship_country": "中国",
        "ship_size": 115.4,
        "ship_model": "散货船",
        "ship_weight": 19000.0,
        "ship_build_date": "2008-09-01",
        "ship_serve_date": "2009-10-01",
        "ship_status": 1,  # 到港
        "ship_longitude": round(random.uniform(112.5, 114.0), 6),
        "ship_latitude": round(random.uniform(23.0, 24.0), 6),
        "ship_text": "嘉航兴是一艘中型散货船。",
    },
    {
        "ship_id": "BINA",
        "ship_name": "安吉6",
        "ship_country": "中国",
        "ship_size": 105.7,
        "ship_model": "滚装船",
        "ship_weight": 18000.0,
        "ship_build_date": "2017-03-10",
        "ship_serve_date": "2018-04-15",
        "ship_status": 1,  # 到港
        "ship_longitude": round(random.uniform(113.0, 114.0), 6),
        "ship_latitude": round(random.uniform(22.8, 23.2), 6),
        "ship_text": "安吉6是一艘滚装船，主要运输汽车。",
    },
]

# # 插入数据到数据库
# for item in ship_data:
#     ShipInfo.objects.create(
#         ship_id=item["ship_id"],
#         ship_name=item["ship_name"],
#         ship_country=item["ship_country"],
#         ship_size=item["ship_size"],
#         ship_model=item["ship_model"],
#         ship_weight=item["ship_weight"],
#         ship_build_date=datetime.strptime(item["ship_build_date"], "%Y-%m-%d"),
#         ship_serve_date=datetime.strptime(item["ship_serve_date"], "%Y-%m-%d"),
#         ship_status=item["ship_status"],
#         ship_longitude=item["ship_longitude"],
#         ship_latitude=item["ship_latitude"],
#         ship_text=item["ship_text"]
#     )

# print("数据插入成功！")

# 修改单条记录
try:
    # 修改 ship_id 为 "BHBO" 的记录
    ship_bhbo = ShipInfo.objects.get(ship_id="BHBO")
    ship_bhbo.ship_status = 2  # 修改状态为 "航行"
    ship_bhbo.save()  # 保存更改
    print(f"船舶 {ship_bhbo.ship_name} 的状态已更新为航行（2）。")

    # 修改 ship_id 为 "BINA" 的记录
    ship_bina = ShipInfo.objects.get(ship_id="BINA")
    ship_bina.ship_status = 2  # 修改状态为 "航行"
    ship_bina.save()  # 保存更改
    print(f"船舶 {ship_bina.ship_name} 的状态已更新为航行（2）。")
except ShipInfo.DoesNotExist as e:
    print("未找到指定的船舶记录！", e)
    