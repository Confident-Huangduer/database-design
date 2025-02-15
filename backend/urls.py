from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    LoginView, RegisterView, PortInfoListView, PortInfoDetailView,
    ShipInfoListView, ShipInfoDetailView, DockedShipsByPortView,
    DockedShipsByShipView, MarineWeatherListView, VoyageByShipView,
    CurrentDepartureByShipView, LogByShipView, VoyageView
)

urlpatterns = [
    # 用户相关
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    # 港口相关
    path('ports/', PortInfoListView.as_view(), name='port-list'),
    path('ports/<str:port_id>/', PortInfoDetailView.as_view(), name='port-detail'),

    # 船舶相关
    path('ships/', ShipInfoListView.as_view(), name='ship-list'),
    path('ships/<str:ship_id>/', ShipInfoDetailView.as_view(), name='ship-detail'),

    # 停靠相关
    path('docked/port/<str:port_id>/', DockedShipsByPortView.as_view(), name='docked-by-port'),
    path('docked/ship/<str:ship_id>/', DockedShipsByShipView.as_view(), name='docked-by-ship'),

    # 天气相关
    path('weather/', MarineWeatherListView.as_view(), name='weather-list'),

    # 航迹相关
    path('voyages/', VoyageView.as_view(), name='voyages'),
    path('voyages/ship/<str:ship_id>/', VoyageByShipView.as_view(), name='voyages-by-ship'),
    path('departures/ship/<str:ship_id>/', CurrentDepartureByShipView.as_view(), name='departure-by-ship'),
    path('logs/ship/<str:ship_id>/', LogByShipView.as_view(), name='logs-by-ship'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 静态文件和媒体文件路由
