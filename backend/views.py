from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    UserInfo, PortInfo, ShipInfo, DockedShip, DepartedShip,
    MarineWeather, VoyageInfo, LogInfo
)
from .serializers import (
    UserInfoSerializer, PortInfoSerializer, ShipInfoSerializer, 
    DockedShipSerializer, DepartedShipSerializer, MarineWeatherSerializer, 
    VoyageInfoSerializer, LogInfoSerializer
)
from django.contrib.auth.hashers import make_password, check_password

# 用户登录视图
class LoginView(APIView):
    def post(self, request):
        useremail = request.data.get('user_email')  # 用户通过 email 登录
        password = request.data.get('user_password')  # 密码

        try:
            # 根据 email 查询用户
            user = UserInfo.objects.get(user_email=useremail)  # email 是唯一的
            # 验证密码
            if check_password(password, user.user_password):
                # 登录成功，返回用户的姓名和电子邮箱
                return Response({
                    "code": 1,
                    "message": "Login successful",
                    "user_name": user.user_name,
                    "user_email": user.user_email
                }, status=status.HTTP_200_OK)
            else:
                # 密码无效
                return Response({"code": 2, "message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        except UserInfo.DoesNotExist:
            # 用户不存在
            return Response({"code": 0, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# 用户注册视图
class RegisterView(APIView):
    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_password=make_password(request.data.get('user_password')))
            return Response({"code": 1, "message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response({"code": 0, "message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# 获取所有港口信息
class PortInfoListView(APIView):
    def get(self, request):
        try:
            ports = PortInfo.objects.all()  # 查询所有港口信息
            serializer = PortInfoSerializer(ports, many=True)  # 序列化数据
            return Response(serializer.data, status=status.HTTP_200_OK)  # 返回序列化数据
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # 返回错误信息

# 获取特定港口信息
class PortInfoDetailView(APIView):
    def get(self, request, port_id):
        try:
            port = PortInfo.objects.get(port_id=port_id)
            serializer = PortInfoSerializer(port)
            return Response({"code": 1, "data": serializer.data}, status=status.HTTP_200_OK)
        except PortInfo.DoesNotExist:
            return Response({"code": -1, "message": "Port not found"}, status=status.HTTP_404_NOT_FOUND)

# 获取所有船舶信息
class ShipInfoListView(APIView):
    def get(self, request):
        ships = ShipInfo.objects.all()
        serializer = ShipInfoSerializer(ships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 获取特定船舶信息
class ShipInfoDetailView(APIView):
    def get(self, request, ship_id):
        try:
            ship = ShipInfo.objects.get(ship_id=ship_id)
            serializer = ShipInfoSerializer(ship)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ShipInfo.DoesNotExist:
            return Response({"message": "Ship not found"}, status=status.HTTP_404_NOT_FOUND)

# 获取某个港口的到港船舶信息
class DockedShipsByPortView(APIView):
    def get(self, request, port_id):
        try:
            # 查询 DockedShip 表中 port_id 对应的所有记录
            docked_ships = DockedShip.objects.filter(port_id=port_id)
            if not docked_ships.exists():
                return Response({"code": -1, "message": "No ships found for this port"}, status=status.HTTP_404_NOT_FOUND)
            
            # 获取所有 ship_id
            ship_ids = docked_ships.values_list('ship_id', flat=True)
            
            # 查询 ShipInfo 表中对应的 ship_id 的详细信息
            ships = ShipInfo.objects.filter(ship_id__in=ship_ids)
            serializer = ShipInfoSerializer(ships, many=True)
            print(serializer.data)
            return Response({"code": 1, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"code": -1, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 获取某个船舶的到港信息
class DockedShipsByShipView(APIView):
    def get(self, request, ship_id):
        try:
            # 查询指定船舶的到港记录
            docked_ships = DockedShip.objects.filter(ship_id=ship_id).select_related('port_id')

            # 如果没有记录，返回 404
            if not docked_ships.exists():
                return Response({"code": -1, "message": "No arrival records found for this ship"}, status=status.HTTP_404_NOT_FOUND)

            # 序列化到港记录，并添加港口信息
            data = []
            for docked_ship in docked_ships:
                data.append({
                    "port_name": docked_ship.port_id.port_name,  # 获取关联的港口名称
                    "arrive_time": docked_ship.arrive_time,  # 获取到港时间
                })

            # 返回数据
            return Response({"code": 1, "arrive_status": data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"code": -1, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取所有气象天气信息
class MarineWeatherListView(APIView):
    def get(self, request):
        weather = MarineWeather.objects.all()
        serializer = MarineWeatherSerializer(weather, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 获取某个船舶的轨迹
class VoyageByShipView(APIView):
    def get(self, request, ship_id):
        try:
            # 查询所有该船的航迹，并预加载关联表
            voyages = VoyageInfo.objects.filter(ship_id=ship_id).select_related('departure', 'destination')

            # 如果没有找到航迹记录，返回 404
            if not voyages.exists():
                return Response({"code": -1, "message": "No voyage records found for this ship"}, status=status.HTTP_404_NOT_FOUND)

            # 构造返回数据
            voyage_list = []
            for voyage in voyages:
                voyage_list.append({
                    "start_time": voyage.start_time,
                    "departure": {
                        "port_id": voyage.departure.port_id,
                        "port_name": voyage.departure.port_name,
                        "port_latitude": voyage.departure.port_latitude,
                        "port_longitude": voyage.departure.port_longitude
                    },
                    "destination": {
                        "port_id": voyage.destination.port_id,
                        "port_name": voyage.destination.port_name,
                        "port_latitude": voyage.destination.port_latitude,
                        "port_longitude": voyage.destination.port_longitude
                    }
                })

            # 返回数据
            return Response({"code": 1, "voyages": voyage_list}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"code": -1, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取所有船舶的轨迹
class VoyageView(APIView):
    def get(self, request):
        try:
            # 查询所有航迹信息并预加载关联表，减少数据库查询次数
            voyages = VoyageInfo.objects.select_related('ship_id', 'departure', 'destination').all()

            # 构造返回的数据格式
            voyage_list = []
            for voyage in voyages:
                voyage_list.append({
                    "ship_id": voyage.ship_id.ship_id,
                    "ship_name": voyage.ship_id.ship_name,
                    "ship_model": voyage.ship_id.ship_model,
                    "ship_latitude": voyage.ship_id.ship_latitude,
                    "ship_longitude": voyage.ship_id.ship_longitude,
                    "start_time": voyage.start_time,
                    "departure": {
                        "port_id": voyage.departure.port_id,
                        "port_name": voyage.departure.port_name
                    },
                    "destination": {
                        "port_id": voyage.destination.port_id,
                        "port_name": voyage.destination.port_name
                    }
                })

            # 返回数据
            return Response({"data": voyage_list}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# 获取某个船舶的当前离港信息
class CurrentDepartureByShipView(APIView):
    def get(self, request, ship_id):
        departures = DepartedShip.objects.filter(ship_id=ship_id)
        serializer = DepartedShipSerializer(departures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 获取某个船舶的历史轨迹日志
class LogByShipView(APIView):
    def get(self, request, ship_id):
        try:
            # 从 VoyageInfo 中获取所有该船舶的 voyage_id
            voyages = VoyageInfo.objects.filter(ship_id=ship_id)
            if not voyages.exists():
                return Response({"code": -1, "message": "No voyage found for this ship"}, status=status.HTTP_404_NOT_FOUND)

            # 获取 voyage_id 列表
            voyage_ids = voyages.values_list('voyage_id', flat=True)

            # 查询 LogInfo 中对应的日志记录，并按时间排序
            logs = LogInfo.objects.filter(voyage_id__in=voyage_ids).order_by('log_time')
            if not logs.exists():
                return Response({"code": -1, "message": "No logs found for this ship"}, status=status.HTTP_404_NOT_FOUND)

            # 序列化日志数据
            serializer = LogInfoSerializer(logs, many=True)

            # 返回数据
            print(serializer.data)
            return Response({"code": 1, "logs": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            # 捕获异常并返回错误信息
            return Response({"code": -1, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

