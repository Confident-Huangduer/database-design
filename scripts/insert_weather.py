import os
import django
import random
from datetime import datetime, timedelta
import sys

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ship_track.settings')
django.setup()

from backend.models import MarineWeather  # 替换为您的 app 名称和模型路径

# 生成随机时间戳
def generate_random_timestamp():
    start_time = datetime(2023, 1, 1, 0, 0, 0)  # 起始时间
    end_time = datetime(2023, 12, 31, 23, 59, 59)  # 结束时间
    delta = end_time - start_time
    random_seconds = random.randint(0, int(delta.total_seconds()))  # 转换为整数
    return start_time + timedelta(seconds=random_seconds)

# 模拟海洋天气数据生成函数
def generate_marine_weather_data():
    weather_data = []
    for _ in range(10):  # 生成 10 条数据
        data = {
            "weather_longitude": round(random.uniform(105.0, 125.0), 3),  # 经度：中国附近
            "weather_latitude": round(random.uniform(15.0, 40.0), 3),  # 纬度：中国附近
            "weather_timestamp": generate_random_timestamp(),  # 随机时间戳
            "temperature": round(random.uniform(15.0, 35.0), 1),  # 气温 (15°C - 35°C)
            "pressure": round(random.uniform(980.0, 1050.0), 1),  # 气压 (980 hPa - 1050 hPa)
            "wave_height": round(random.uniform(0.5, 5.0), 1),  # 波浪高度 (0.5m - 5m)
            "wave_period": round(random.uniform(3.0, 10.0), 1),  # 波浪周期 (3s - 10s)
            "wave_temperature": round(random.uniform(10.0, 30.0), 1),  # 波浪温度 (10°C - 30°C)
            "wind_speed": round(random.uniform(0.5, 20.0), 1),  # 风速 (0.5 m/s - 20 m/s)
            "wind_direction": round(random.uniform(0, 360), 1),  # 风向 (0° - 360°)
            "impact_area": round(random.uniform(100.0, 1000.0), 1),  # 影响面积 (100 km² - 1000 km²)
        }
        weather_data.append(data)
    return weather_data

# 插入数据到数据库
def insert_marine_weather_data():
    weather_data = generate_marine_weather_data()
    for item in weather_data:
        MarineWeather.objects.create(
            weather_longitude=item["weather_longitude"],
            weather_latitude=item["weather_latitude"],
            weather_timestamp=item["weather_timestamp"],
            temperature=item["temperature"],
            pressure=item["pressure"],
            wave_height=item["wave_height"],
            wave_period=item["wave_period"],
            wave_temperature=item["wave_temperature"],
            wind_speed=item["wind_speed"],
            wind_direction=item["wind_direction"],
            impact_area=item["impact_area"]
        )
    print("海洋天气数据插入成功！")

if __name__ == "__main__":
    insert_marine_weather_data()
