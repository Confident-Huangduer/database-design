import os
import django
import sys

# 设置 Django 项目环境
# 将项目根目录添加到 PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ship_track.settings')
django.setup()

from backend.models import PortInfo

# 数据列表
data = [
    {
        "port_id": "CNSGH",
        "port_name": "上海港",
        "port_country": "中国",
        "port_build_date": "1996-01-01",
        "port_longitude": 121.19,
        "port_latitude": 31.14,
        "port_depth": 10.0,
        "port_area": 3620.2,
        "port_text": "上海港（Shanghai Port），是中国上海市港口，位于中国大陆海岸线中部、长江入海口处，前通中国南北沿海和世界大洋，后贯长江流域和江浙皖内河、太湖流域。",
        "port_img": "img/CNSGH.jpg"
    },
    {
        "port_id": "CNZOS",
        "port_name": "宁波舟山港",
        "port_country": "中国",
        "port_build_date": "2001-01-01",
        "port_longitude": 121.50,
        "port_latitude": 29.56,
        "port_depth": 17.0,
        "port_area": 600.0,
        "port_text": "宁波舟山港是世界第一大港，货物吞吐量位居全球首位。",
        "port_img": None
    },
    {
        "port_id": "CNSZX",
        "port_name": "深圳港",
        "port_country": "中国",
        "port_build_date": "2001-01-01",
        "port_longitude": 114.40,
        "port_latitude": 22.31,
        "port_depth": 16.0,
        "port_area": 260.0,
        "port_text": "深圳港是中国南方的重要港口，毗邻香港。",
        "port_img": None
    },
    {
        "port_id": "CNQIN",
        "port_name": "青岛港",
        "port_country": "中国",
        "port_build_date": "2001-01-01",
        "port_longitude": 120.19,
        "port_latitude": 36.04,
        "port_depth": 15.0,
        "port_area": 220.0,
        "port_text": "青岛港是中国东部的重要港口，位于山东半岛南岸。",
        "port_img": None
    },
    {
        "port_id": "CNGGZ",
        "port_name": "广州港",
        "port_country": "中国",
        "port_build_date": "2001-01-01",
        "port_longitude": 113.36,
        "port_latitude": 23.06,
        "port_depth": 14.0,
        "port_area": 300.0,
        "port_text": "广州港是中国华南地区最大的港口，历史悠久。",
        "port_img": None
    }
]

# 插入数据到数据库
for item in data:
    PortInfo.objects.create(
        port_id=item["port_id"],
        port_name=item["port_name"],
        port_country=item["port_country"],
        port_build_date=item["port_build_date"],
        port_longitude=item["port_longitude"],
        port_latitude=item["port_latitude"],
        port_depth=item["port_depth"],
        port_area=item["port_area"],
        port_text=item["port_text"],
        port_img=item["port_img"]
    )

print("数据插入成功！")
