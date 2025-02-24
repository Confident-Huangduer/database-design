# Generated by Django 5.1.4 on 2025-01-04 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MarineWeather",
            fields=[
                (
                    "weather_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="天气编号"
                    ),
                ),
                ("longitude", models.FloatField(verbose_name="经度")),
                ("latitude", models.FloatField(verbose_name="纬度")),
                ("timestamp", models.DateTimeField(verbose_name="时间戳")),
                ("temperature", models.FloatField(verbose_name="气温")),
                ("pressure", models.FloatField(verbose_name="气压")),
                ("wave_height", models.FloatField(verbose_name="波浪高度")),
                ("wave_period", models.FloatField(verbose_name="波浪周期")),
                ("wave_temperature", models.FloatField(verbose_name="波浪温度")),
                ("wind_speed", models.FloatField(verbose_name="风速")),
                ("wind_direction", models.FloatField(verbose_name="风向")),
                ("impact_area", models.FloatField(verbose_name="影响面积")),
            ],
            options={
                "verbose_name": "海洋天气",
                "verbose_name_plural": "海洋天气",
                "db_table": "MarineWeather",
            },
        ),
        migrations.CreateModel(
            name="PortInfo",
            fields=[
                (
                    "port_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="港口编号"
                    ),
                ),
                (
                    "port_name",
                    models.CharField(max_length=100, verbose_name="港口名称"),
                ),
                (
                    "port_country",
                    models.CharField(max_length=50, verbose_name="所属国家"),
                ),
                ("port_build_date", models.DateField(verbose_name="建造日期")),
                ("port_longitude", models.FloatField(verbose_name="所在经度")),
                ("port_latitude", models.FloatField(verbose_name="所在纬度")),
                ("port_depth", models.FloatField(verbose_name="港口深度")),
                ("port_area", models.FloatField(verbose_name="港口面积")),
                (
                    "port_text",
                    models.CharField(
                        default="暂无详细描述", max_length=300, verbose_name="港口描述"
                    ),
                ),
                (
                    "port_img",
                    models.ImageField(
                        blank=True,
                        default=None,
                        upload_to="img/",
                        verbose_name="港口图片",
                    ),
                ),
            ],
            options={
                "verbose_name": "港口信息",
                "verbose_name_plural": "港口信息列表",
                "db_table": "PortInfo",
            },
        ),
        migrations.CreateModel(
            name="ShipInfo",
            fields=[
                (
                    "ship_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="船舶呼号"
                    ),
                ),
                (
                    "ship_name",
                    models.CharField(max_length=100, verbose_name="船舶名称"),
                ),
                (
                    "ship_country",
                    models.CharField(max_length=50, verbose_name="所属国家"),
                ),
                ("ship_size", models.FloatField(verbose_name="船舶尺寸")),
                (
                    "ship_model",
                    models.CharField(max_length=100, verbose_name="船舶型号"),
                ),
                ("ship_weight", models.FloatField(verbose_name="船舶重量")),
                ("ship_build_date", models.DateField(verbose_name="建造日期")),
                ("ship_serve_date", models.DateField(verbose_name="服役日期")),
                (
                    "ship_status",
                    models.SmallIntegerField(
                        choices=[(1, "到港"), (2, "航行")], verbose_name="船舶状态"
                    ),
                ),
                ("ship_longitude", models.FloatField(verbose_name="所在经度")),
                ("ship_latitude", models.FloatField(verbose_name="所在纬度")),
                ("ship_text", models.TextField(verbose_name="描述信息")),
            ],
            options={
                "verbose_name": "船舶信息",
                "verbose_name_plural": "船舶信息",
                "db_table": "ShipInfo",
            },
        ),
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "user_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="用户ID"
                    ),
                ),
                ("user_name", models.CharField(max_length=100, verbose_name="用户名")),
                (
                    "user_password",
                    models.CharField(max_length=255, verbose_name="用户密码"),
                ),
                (
                    "user_email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="用户邮箱"
                    ),
                ),
                (
                    "user_role",
                    models.CharField(
                        choices=[("user", "普通用户"), ("admin", "管理员")],
                        default="user",
                        max_length=50,
                        verbose_name="用户角色",
                    ),
                ),
            ],
            options={
                "verbose_name": "用户信息",
                "verbose_name_plural": "用户信息",
                "db_table": "UserInfo",
            },
        ),
        migrations.CreateModel(
            name="DockedShip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("arrive_time", models.DateTimeField(verbose_name="到港时间")),
                ("leave_time", models.DateTimeField(verbose_name="离港时间")),
                (
                    "port_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.portinfo",
                        verbose_name="港口编号",
                    ),
                ),
                (
                    "ship_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.shipinfo",
                        verbose_name="船舶呼号",
                    ),
                ),
            ],
            options={
                "verbose_name": "停靠船舶",
                "verbose_name_plural": "停靠船舶",
                "db_table": "DockedShip",
            },
        ),
        migrations.CreateModel(
            name="DepartedShip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("departure", models.CharField(max_length=64, verbose_name="出发地")),
                ("destination", models.CharField(max_length=64, verbose_name="目的地")),
                ("leave_time", models.DateTimeField(verbose_name="离港时间")),
                (
                    "expected_arrive_time",
                    models.DateTimeField(verbose_name="预计到港时间"),
                ),
                (
                    "ship_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.shipinfo",
                        verbose_name="船舶呼号",
                    ),
                ),
            ],
            options={
                "verbose_name": "离港船舶",
                "verbose_name_plural": "离港船舶",
                "db_table": "DepartedShip",
            },
        ),
        migrations.CreateModel(
            name="VoyageInfo",
            fields=[
                (
                    "voyage_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="航迹编号"
                    ),
                ),
                ("start_time", models.DateTimeField(verbose_name="开始时间")),
                ("end_time", models.DateTimeField(verbose_name="结束时间")),
                (
                    "departure",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="departures",
                        to="backend.portinfo",
                        verbose_name="出发地",
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="destinations",
                        to="backend.portinfo",
                        verbose_name="目的地",
                    ),
                ),
                (
                    "ship_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.shipinfo",
                        verbose_name="船舶呼号",
                    ),
                ),
            ],
            options={
                "verbose_name": "航迹信息",
                "verbose_name_plural": "航迹信息",
                "db_table": "VoyageInfo",
            },
        ),
        migrations.CreateModel(
            name="LogInfo",
            fields=[
                (
                    "log_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="日志编号"
                    ),
                ),
                ("log_time", models.DateTimeField(verbose_name="记录时间")),
                ("ship_longitude", models.FloatField(verbose_name="所在经度")),
                ("ship_latitude", models.FloatField(verbose_name="所在纬度")),
                ("ship_speed", models.FloatField(verbose_name="船舶速度")),
                ("ship_direction", models.FloatField(verbose_name="船舶方向")),
                (
                    "voyage_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.voyageinfo",
                        verbose_name="航迹编号",
                    ),
                ),
            ],
            options={
                "verbose_name": "日志信息",
                "verbose_name_plural": "日志信息",
                "db_table": "LogInfo",
            },
        ),
    ]
