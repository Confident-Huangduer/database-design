from rest_framework import serializers
from .models import (
    UserInfo, ShipInfo, PortInfo, DockedShip, DepartedShip,
    MarineWeather, VoyageInfo, LogInfo
)

# 用户信息序列化器
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'  # 序列化所有字段
        read_only_fields = ('user_id',)  # user_id 只读

# 船舶信息序列化器
class ShipInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipInfo
        fields = '__all__'
        read_only_fields = ('ship_id',)  # ship_id 只读

# 港口信息序列化器
class PortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortInfo
        fields = '__all__'
        read_only_fields = ('port_id',)  # port_id 只读

# 停靠船舶序列化器
class DockedShipSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship_id.ship_name', read_only=True)  # 显示船舶名称
    port_name = serializers.CharField(source='port_id.port_name', read_only=True)  # 显示港口名称

    class Meta:
        model = DockedShip
        fields = '__all__'

# 离港船舶序列化器
class DepartedShipSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship_id.ship_name', read_only=True)  # 显示船舶名称

    class Meta:
        model = DepartedShip
        fields = '__all__'

# 海洋天气信息序列化器
class MarineWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarineWeather
        fields = '__all__'
        read_only_fields = ('weather_id',)  # weather_id 只读

# 航迹信息序列化器
class VoyageInfoSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship_id.ship_name', read_only=True)  # 显示船舶名称
    departure_name = serializers.CharField(source='departure.port_name', read_only=True)  # 显示出发地港口名称
    destination_name = serializers.CharField(source='destination.port_name', read_only=True)  # 显示目的地港口名称

    class Meta:
        model = VoyageInfo
        fields = '__all__'
        read_only_fields = ('voyage_id',)  # voyage_id 只读

# 日志信息序列化器
class LogInfoSerializer(serializers.ModelSerializer):
    voyage_name = serializers.CharField(source='voyage_id.voyage_id', read_only=True)  # 显示航迹编号

    class Meta:
        model = LogInfo
        fields = '__all__'
        read_only_fields = ('log_id',)  # log_id 只读
