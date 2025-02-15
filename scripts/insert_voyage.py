import os
import django
from datetime import datetime
from django.utils import timezone
import sys

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ship_track.settings')
django.setup()

from backend.models import VoyageInfo, ShipInfo, PortInfo  # 替换为您的 app 名称和模型路径

# 插入航迹信息
def insert_voyages():
    voyages = [
        {
            "ship_id": "BAHL",
            "departure_port_id": "CNSGH",
            "destination_port_id": "CNZOS",
            "start_time": datetime(2025, 1, 1, 8, 0, 0),
            "end_time": None,  # 表示航行中，没有结束时间
        },
        {
            "ship_id": "BHBO",
            "departure_port_id": "CNSGH",
            "destination_port_id": "CNQIN",
            "start_time": datetime(2025, 1, 3, 10, 0, 0),
            "end_time": None,  # 表示航行中，没有结束时间
        },
        {
            "ship_id": "BINA",
            "departure_port_id": "CNSZX",
            "destination_port_id": "CNZOS",
            "start_time": datetime(2025, 1, 5, 7, 0, 0),
            "end_time": None,  # 表示航行中，没有结束时间
        },
    ]

    for voyage_data in voyages:
        try:
            # 查询外键记录
            ship = ShipInfo.objects.get(ship_id=voyage_data["ship_id"])
            departure_port = PortInfo.objects.get(port_id=voyage_data["departure_port_id"])
            destination_port = PortInfo.objects.get(port_id=voyage_data["destination_port_id"])

            # 创建航迹记录
            voyage = VoyageInfo(
                ship_id=ship,
                departure=departure_port,
                destination=destination_port,
                start_time=timezone.make_aware(voyage_data["start_time"]),  # 转换为 aware datetime
                end_time=voyage_data["end_time"],  # 设置为 None
            )
            voyage.save()
            print(
                f"航迹 {voyage.voyage_id} 插入成功：船舶 {ship.ship_name} 从 {departure_port.port_name} 开往 {destination_port.port_name}"
            )

        except ShipInfo.DoesNotExist:
            print(f"船舶 {voyage_data['ship_id']} 记录不存在！")
        except PortInfo.DoesNotExist:
            print(f"港口 {voyage_data['departure_port_id']} 或 {voyage_data['destination_port_id']} 记录不存在！")
        except Exception as e:
            print(f"插入航迹时发生错误：{e}")

if __name__ == "__main__":
    insert_voyages()
