import os
import django
import sys
from datetime import datetime
from django.utils import timezone

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ship_track.settings')
django.setup()

from backend.models import DockedShip, ShipInfo, PortInfo  # 替换为您的 app 名称和模型路径

# 插入停靠船舶数据
def insert_docked_ships():
    try:
        # 获取船舶和港口记录
        ship_baks = ShipInfo.objects.get(ship_id="BAKS")  # 船舶编号 BAKS
        port_cnsgh = PortInfo.objects.get(port_id="CNSGH")  # 港口编号 CNSGH

        ship_bfeo = ShipInfo.objects.get(ship_id="BFEO")  # 船舶编号 BFEO
        port_cnqin = PortInfo.objects.get(port_id="CNQIN")  # 港口编号 CNQIN

        # 插入记录 1
        docked_ship_1 = DockedShip(
            ship_id=ship_baks,
            port_id=port_cnsgh,
            arrive_time=timezone.make_aware(datetime(2025, 1, 1, 0, 0, 0)),  # aware datetime
            leave_time=None  # 表示尚未离港
        )
        docked_ship_1.save()
        print(f"记录 1 插入成功：船舶 {ship_baks.ship_name} 到达港口 {port_cnsgh.port_name}")

        # 插入记录 2
        docked_ship_2 = DockedShip(
            ship_id=ship_bfeo,
            port_id=port_cnqin,
            arrive_time=timezone.make_aware(datetime(2025, 1, 2, 0, 0, 0)),  # aware datetime
            leave_time=None  # 表示尚未离港
        )
        docked_ship_2.save()
        print(f"记录 2 插入成功：船舶 {ship_bfeo.ship_name} 到达港口 {port_cnqin.port_name}")

    except ShipInfo.DoesNotExist as e:
        print(f"船舶记录不存在：{e}")
    except PortInfo.DoesNotExist as e:
        print(f"港口记录不存在：{e}")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    insert_docked_ships()
