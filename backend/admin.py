from django.contrib import admin
from .models import (
    UserInfo, ShipInfo, PortInfo, DockedShip, DepartedShip,
    MarineWeather, VoyageInfo, LogInfo
)

# 用户信息表配置
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_email', 'user_role')  # 列表页显示字段
    search_fields = ('user_name', 'user_email')  # 添加搜索框
    list_filter = ('user_role',)  # 过滤器
    ordering = ('user_id',)  # 按用户ID排序

# 船舶信息表配置
@admin.register(ShipInfo)
class ShipInfoAdmin(admin.ModelAdmin):
    list_display = ('ship_id', 'ship_name', 'ship_country', 'ship_status')  # 列表页显示字段
    search_fields = ('ship_name', 'ship_country')  # 搜索框
    list_filter = ('ship_status', 'ship_country')  # 过滤器
    ordering = ('ship_id',)  # 排序
    fieldsets = (  # 分组显示字段
        ('基本信息', {
            'fields': ('ship_name', 'ship_country', 'ship_model', 'ship_size', 'ship_weight')
        }),
        ('状态信息', {
            'fields': ('ship_status', 'ship_longitude', 'ship_latitude', 'ship_text')
        }),
        ('时间信息', {
            'fields': ('ship_build_date', 'ship_serve_date')
        }),
    )

# 港口信息表配置
@admin.register(PortInfo)
class PortInfoAdmin(admin.ModelAdmin):
    list_display = ('port_id', 'port_name', 'port_country', 'port_depth', 'port_area')  # 列表页显示字段
    search_fields = ('port_name', 'port_country')  # 搜索框
    list_filter = ('port_country',)  # 过滤器
    ordering = ('port_id',)  # 排序
    readonly_fields = ('port_img',)  # 图片只读
    fieldsets = (  # 分组显示字段
        ('基本信息', {
            'fields': ('port_name', 'port_country', 'port_depth', 'port_area')
        }),
        ('位置信息', {
            'fields': ('port_longitude', 'port_latitude')
        }),
        ('其他信息', {
            'fields': ('port_text', 'port_img')
        }),
    )

# 停靠船舶表配置
@admin.register(DockedShip)
class DockedShipAdmin(admin.ModelAdmin):
    list_display = ('ship_id', 'port_id', 'arrive_time', 'leave_time')  # 列表页显示字段
    search_fields = ('ship_id__ship_name', 'port_id__port_name')  # 通过外键的名称搜索
    list_filter = ('arrive_time', 'leave_time')  # 过滤器
    ordering = ('arrive_time',)  # 排序

# 离港船舶表配置
@admin.register(DepartedShip)
class DepartedShipAdmin(admin.ModelAdmin):
    list_display = ('ship_id', 'departure', 'destination', 'leave_time', 'expected_arrive_time')  # 列表页显示字段
    search_fields = ('ship_id__ship_name', 'departure', 'destination')  # 通过外键的名称搜索
    list_filter = ('departure', 'destination', 'leave_time')  # 过滤器
    ordering = ('leave_time',)  # 排序

# 海洋天气表配置
@admin.register(MarineWeather)
class MarineWeatherAdmin(admin.ModelAdmin):
    list_display = ('weather_id', 'weather_longitude', 'weather_latitude', 'weather_timestamp', 'temperature', 'pressure', 'wave_height')  # 列表页显示字段
    search_fields = ('weather_id',)  # 搜索框
    list_filter = ('weather_timestamp',)  # 过滤器
    ordering = ('weather_timestamp',)  # 排序

# 航迹信息表配置
class LogInfoInline(admin.TabularInline):  # 内联日志信息
    model = LogInfo
    extra = 0

@admin.register(VoyageInfo)
class VoyageInfoAdmin(admin.ModelAdmin):
    list_display = ('voyage_id', 'ship_id', 'departure', 'destination', 'start_time', 'end_time')  # 列表页显示字段
    search_fields = ('ship_id__ship_name', 'departure__port_name', 'destination__port_name')  # 搜索框
    list_filter = ('start_time', 'end_time')  # 过滤器
    ordering = ('voyage_id',)  # 排序
    inlines = [LogInfoInline]  # 内联日志信息

# 日志信息表配置
@admin.register(LogInfo)
class LogInfoAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'voyage_id', 'log_time', 'ship_longitude', 'ship_latitude', 'ship_speed', 'ship_direction')  # 列表页显示字段
    search_fields = ('voyage_id__voyage_id',)  # 搜索框
    list_filter = ('log_time',)  # 过滤器
    ordering = ('log_time',)  # 排序
