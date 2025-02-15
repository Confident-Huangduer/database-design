import os
import django
import random
import sys
from datetime import timedelta
from django.utils import timezone

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ship_track.settings')
django.setup()

from backend.models import LogInfo, VoyageInfo  # 替换为您的应用名称和模型路径

# 港口信息
PORTS = {
    "CNSGH": {"longitude": 121.19, "latitude": 31.14},  # 上海港
    "CNZOS": {"longitude": 121.50, "latitude": 29.56},  # 宁波舟山港
    "CNSZX": {"longitude": 114.40, "latitude": 22.31},  # 深圳港
    "CNQIN": {"longitude": 120.19, "latitude": 36.04},  # 青岛港
    "CNGGZ": {"longitude": 113.36, "latitude": 23.06},  # 广州港
}

# 插入日志信息
def generate_logs():
    try:
        # 获取所有未完成的航迹（没有结束时间的航迹）
        voyages = VoyageInfo.objects.filter(end_time__isnull=True)

        for voyage in voyages:
            # 获取出发地和目的地经纬度
            departure_port = PORTS.get(voyage.departure.port_id)
            destination_port = PORTS.get(voyage.destination.port_id)

            if not departure_port or not destination_port:
                print(f"航迹 {voyage.voyage_id} 的港口信息缺失，无法生成日志。")
                continue

            # 出发港口和目的港口的经纬度
            dep_longitude, dep_latitude = departure_port["longitude"], departure_port["latitude"]
            dest_longitude, dest_latitude = destination_port["longitude"], destination_port["latitude"]

            # 模拟航行中的经纬度变化
            longitude_step = (dest_longitude - dep_longitude) / 7  # 每次日志的经度增量
            latitude_step = (dest_latitude - dep_latitude) / 7  # 每次日志的纬度增量

            # 模拟时间间隔
            start_time = voyage.start_time
            log_interval = timedelta(hours=1)  # 每条日志间隔 1 小时

            # 初始值
            current_longitude = dep_longitude
            current_latitude = dep_latitude
            current_time = start_time
            current_speed = random.uniform(10, 20)  # 船舶速度 (10 - 20 节)
            current_direction = random.uniform(0, 360)  # 船舶方向 (0 - 360°)

            # 生成 7 条日志数据
            for i in range(7):
                # 插入日志记录
                log = LogInfo(
                    voyage_id=voyage,
                    log_time=current_time,
                    ship_longitude=round(current_longitude, 6),
                    ship_latitude=round(current_latitude, 6),
                    ship_speed=round(current_speed, 2),
                    ship_direction=round(current_direction, 2),
                )
                log.save()
                print(
                    f"日志 {log.log_id} 插入成功：航迹 {voyage.voyage_id}，时间 {current_time}，经度 {current_longitude}，纬度 {current_latitude}，速度 {current_speed} 节，方向 {current_direction}°"
                )

                # 更新到下一次的值
                current_longitude += longitude_step + random.uniform(-0.02, 0.02)  # 加入微小随机偏差
                current_latitude += latitude_step + random.uniform(-0.02, 0.02)  # 加入微小随机偏差
                current_time += log_interval
                current_speed = max(5, min(25, current_speed + random.uniform(-1, 1)))  # 保证速度在 5 - 25 节之间
                current_direction = (current_direction + random.uniform(-10, 10)) % 360  # 保证方向在 0 - 360°

    except VoyageInfo.DoesNotExist as e:
        print(f"航迹记录不存在：{e}")
    except Exception as e:
        print(f"插入日志信息时发生错误：{e}")

if __name__ == "__main__":
    generate_logs()
