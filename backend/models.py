from django.db import models

# Create your models here.

# 用户信息表
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name="用户ID")
    user_name = models.CharField(max_length=100, verbose_name="用户名")
    user_password = models.CharField(max_length=255, verbose_name="用户密码")
    user_email = models.EmailField(unique=True, verbose_name="用户邮箱")
    USER_ROLE_CHOICES = [
        ('user', '普通用户'),
        ('admin', '管理员'),
    ]
    user_role = models.CharField(
        max_length=50, 
        choices=USER_ROLE_CHOICES, 
        default='user', 
        verbose_name="用户角色"
    )

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = "UserInfo"

    def __str__(self):
        return self.user_name

# 船舶信息表
class ShipInfo(models.Model):
    ship_id = models.CharField(max_length=20, primary_key=True, verbose_name="船舶呼号")
    ship_name = models.CharField(max_length=100, verbose_name="船舶名称")
    ship_country = models.CharField(max_length=50, verbose_name="所属国家")
    ship_size = models.FloatField(verbose_name="船舶尺寸")
    ship_model = models.CharField(max_length=100, verbose_name="船舶型号")
    ship_weight = models.FloatField(verbose_name="船舶重量")
    ship_build_date = models.DateField(verbose_name="建造日期")
    ship_serve_date = models.DateField(verbose_name="服役日期")
    ship_status_choice = (
        (1, "到港"),
        (2, "航行")
    )
    ship_status = models.SmallIntegerField(verbose_name='船舶状态', choices=ship_status_choice)

    ship_longitude = models.FloatField(verbose_name="所在经度")
    ship_latitude = models.FloatField(verbose_name="所在纬度")
    ship_text = models.TextField(verbose_name="描述信息")

    class Meta:
        verbose_name = "船舶信息"
        verbose_name_plural = verbose_name
        db_table = "ShipInfo"

    def __str__(self):
        return self.ship_name

# 港口信息表
class PortInfo(models.Model):
    port_id = models.CharField(max_length=20, primary_key=True, verbose_name="港口编号")
    port_name = models.CharField(max_length=100, verbose_name="港口名称")
    port_country = models.CharField(max_length=50, verbose_name="所属国家")
    port_build_date = models.DateField(verbose_name="建造日期")
    port_longitude = models.FloatField(verbose_name="所在经度")
    port_latitude = models.FloatField(verbose_name="所在纬度")
    port_depth = models.FloatField(verbose_name="港口深度")
    port_area = models.FloatField(verbose_name="港口面积")
    port_text = models.CharField(max_length=300, verbose_name="港口描述", default='暂无详细描述')
    port_img = models.ImageField(verbose_name='港口图片', upload_to='img/', default=None, blank=True)

    class Meta:
        verbose_name = "港口信息"
        verbose_name_plural = verbose_name
        db_table = "PortInfo"

    def __str__(self):
        return self.port_name

# 停靠船舶表
class DockedShip(models.Model):
    ship_id = models.ForeignKey(ShipInfo, on_delete=models.CASCADE, verbose_name="船舶呼号")
    port_id = models.ForeignKey(PortInfo, on_delete=models.CASCADE, verbose_name="港口编号")
    arrive_time = models.DateTimeField(verbose_name="到港时间")
    leave_time = models.DateTimeField(verbose_name="离港时间", null=True, blank=True) # 允许为空

    class Meta:
        verbose_name = "停靠船舶"
        verbose_name_plural = verbose_name
        db_table = "DockedShip"

    def __str__(self):
        return f"船舶 {self.ship_id} 停靠在港口 {self.port_id}"

# 离港船舶表
class DepartedShip(models.Model):
    ship_id = models.ForeignKey(ShipInfo, on_delete=models.CASCADE, verbose_name="船舶呼号")
    departure = models.CharField(verbose_name='出发地', max_length=64)
    destination = models.CharField(verbose_name='目的地', max_length=64)
    leave_time = models.DateTimeField(verbose_name="离港时间")
    expected_arrive_time = models.DateTimeField(verbose_name="预计到港时间")

    class Meta:
        verbose_name = "离港船舶"
        verbose_name_plural = verbose_name
        db_table = "DepartedShip"

    def __str__(self):
        return f"船舶 {self.ship_id} 从港口 {self.start_port_id} 离开，目的地为 {self.end_port_id}"

# 海洋天气信息表
class MarineWeather(models.Model):
    weather_id = models.AutoField(primary_key=True, verbose_name="天气编号")
    weather_longitude = models.FloatField(verbose_name="经度")
    weather_latitude = models.FloatField(verbose_name="纬度")
    weather_timestamp = models.DateTimeField(verbose_name="时间戳")
    temperature = models.FloatField(verbose_name="气温")
    pressure = models.FloatField(verbose_name="气压")
    wave_height = models.FloatField(verbose_name="波浪高度")
    wave_period = models.FloatField(verbose_name="波浪周期")
    wave_temperature = models.FloatField(verbose_name="波浪温度")
    wind_speed = models.FloatField(verbose_name="风速")
    wind_direction = models.FloatField(verbose_name="风向")
    impact_area = models.FloatField(verbose_name="影响面积")

    class Meta:
        verbose_name = "海洋天气"
        verbose_name_plural = verbose_name
        db_table = "MarineWeather"

    def __str__(self):
        return f"天气记录 {self.weather_id} 于 {self.timestamp}"

# 航迹信息表
class VoyageInfo(models.Model):
    voyage_id = models.AutoField(primary_key=True, verbose_name="航迹编号")
    ship_id = models.ForeignKey(ShipInfo, on_delete=models.CASCADE, verbose_name="船舶呼号")
    departure = models.ForeignKey(PortInfo, related_name='departures', on_delete=models.CASCADE, verbose_name='出发地')
    destination = models.ForeignKey(PortInfo, related_name='destinations', on_delete=models.CASCADE, verbose_name='目的地')
    start_time = models.DateTimeField(verbose_name="开始时间", unique=True)
    end_time = models.DateTimeField(verbose_name="结束时间", default=0, null=True, blank=True)

    class Meta:
        verbose_name = "航迹信息"
        verbose_name_plural = verbose_name
        db_table = "VoyageInfo"

    def __str__(self):
        return f"航迹 {self.voyage_id} 属于船舶 {self.ship_id}"

# 日志信息表
class LogInfo(models.Model):
    log_id = models.AutoField(primary_key=True, verbose_name="日志编号")
    voyage_id = models.ForeignKey(VoyageInfo, on_delete=models.CASCADE, verbose_name="航迹编号")
    log_time = models.DateTimeField(verbose_name="记录时间")
    ship_longitude = models.FloatField(verbose_name="所在经度")
    ship_latitude = models.FloatField(verbose_name="所在纬度")
    ship_speed = models.FloatField(verbose_name="船舶速度")
    ship_direction = models.FloatField(verbose_name="船舶方向")

    class Meta:
        verbose_name = "日志信息"
        verbose_name_plural = verbose_name
        db_table = "LogInfo"

    def __str__(self):
        return f"日志 {self.log_id} 对应航迹 {self.voyage_id}"
