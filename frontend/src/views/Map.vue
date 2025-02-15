<template>
    <div id="map" @mousemove="getLocation">
      <el-button type="primary" class="location-bar">经度: {{ formatLatLng(center)[1] }}&nbsp;&nbsp;&nbsp;&nbsp;纬度: {{ formatLatLng(center)[0] }}</el-button>
      <div id="harbors-info" class="hidden">
        <div id="harbor-main-info">
          <div id="harbor-text-info">
            <div id="harbor-name">默认港口</div>
            <div id="harbor-id-country">
              <div id="harbor-id">FFFFF</div>
              <div id="harbor-country">中国</div>
            </div>
            <div id="harbor-info-detail">
              <p id="harbor-year-depth">
                <span id="harbor-year"><strong>建造年份:</strong> 2099 </span>  
                <span id="harbor-depth"><strong>港口水深:</strong> 6 m</span>
              </p>
              <p id="harbor-latitude-longitude" style="margin-top: -10px; ">
                <span id="harbor-latitude"><strong>所处经度:</strong> 22.22 </span> 
                <span id="harbor-longitude"><strong>所处纬度:</strong> 111.11 </span>
              </p>
            </div>
          </div>
          <div id="harbor-photo">
            <img src="@/static/default.png"/>
          </div>
        </div>
        <div id="harbor-summary">
          <strong>港口简介:</strong>暂无
        </div>
      </div>
      <div id="boat-info" class="hidden">
        <div id="boat-name">暂无船舶</div>
        <div id="boat-id-country">
              <div id="boat-id">FFFFF</div>
              <div id="boat-country">中国</div>
        </div>
        <div id="boat-detail">
          <p id="boat-model-weight-size">
            <span id="boat-model"><strong>船舶型号:</strong> 散货船 </span> 
            <span id="boat-weight"><strong>船舶吨位:</strong> 9999 </span>
            <span id="boat-size"><strong>船舶吃水:</strong> 11.11 m </span>
          </p>
          <p id="boat-status-build-serve">
            <span id="boat-status"><strong>当前状态:</strong> 到港 </span>
            <span id="boat-build-date"><strong>建造日期:</strong> 1970-01-01 </span> 
            <span id="boat-serve-date"><strong>服役日期:</strong> 1970-01-01 </span>
          </p>
          <p id="boat-longitude-latitude">
            <span id="boat-longitude"><strong>所处经度:</strong> 22.22 </span>
            <span id="boat-latitude"><strong>所处纬度:</strong> 111.11 </span>
          </p>
        </div>
        <div id="boat-detail-status" v-if="ifArrive">
          <div id="boat-detail-status-text">
            <span id="arrive-harbor"><strong>停靠港口:</strong> 未知 </span >
            <span id="arrive-time"><strong>到港时间:</strong> 未知 </span >
            <span id="leave-time"><strong>离港时间:</strong> 未知 </span >
          </div>
        </div>
        <div id="boat-detail-status-voyage" v-else >
          <p id="boat-departure-destination-time">
            <span id="boat-departure"><strong>出发地:</strong> 暂无 </span>
            <span id="boat-destination"><strong>目的地:</strong> 暂无 </span> 
            <span id="boat-voyage-time"><strong>行驶时间:</strong> -99.99 s </span>
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch} from "vue";
  import { ElMessage } from "element-plus";
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";
  import axios from "../api/axios"; // 修改为实际的 axios 配置路径
  import boatMarkerImage from '@/static/boat_icon.png';
  import harborMarkerImage from '@/static/port_icon.png';
  import weatherMarkerImage from '@/static/weather_icon.png';
  import logMarkerImage from '@/static/log_icon.png';
  
  const props = defineProps(["latitude", "longitude", "ship_latitude", "ship_longitude","showHarbor", "showBoat", "showTrack", "showWeather"]);
  const center = ref([39.54, 116.23]);
  const initialCenter = ref([39.54, 116.23]);
  const map = ref(null);
  const harborsList = ref([]);
  const boatList = ref([])
  const weatherList = ref([])
  const harborsMarkerList = ref([]);
  const boatMarkerList = ref([]);
  let logMarkerList = [];
  const weatherMarkerList = ref([])
  const weatherCircleList = ref([]);
  const ifArrive = ref(false)
  let currentPolyline = null;
  
  
  const getLocation = event => {
    if (map.value) {
      const latlng = map.value.mouseEventToLatLng(event);
      center.value = [latlng.lat, latlng.lng];
      while (center.value[1] < -180) center.value[1] += 360;
      while (center.value[1] > 180) center.value[1] -= 360;
    }
  };
  
  const formatLatLng = latLng => {
    return latLng.map(coord => coord.toFixed(3));
  };
  
  const getPortInfo = async () => {
    try {
      const response = await axios.get("/ports/");
      harborsList.value = response.data;
    }
    catch (error) {
      let errorMessage = "请求错误！";
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage += " 详情: " + error.response.data.detail;
      }
      ElMessage({
        showClose: true,
        message: errorMessage,
        type: "error"
      });
    }
  };
  
  const GetCertainHarbor = async (data) => {
    try {
      const response = await axios.get(`/ports/${data.port_id}/`);
      if (response.data.code === -1) {
        ElMessage({
          showClose: true,
          message: "港口信息查询失败：不存在此港口！",
          type: "error"
        });
        return;
      } else {
        return response.data.data; // 直接返回后端的港口数据
      }
    } catch (error) {
      let errorMessage = "请求错误！";
      if (error.response && error.response.data && error.response.data.message) {
        errorMessage += " 详情: " + error.response.data.message;
      }
      ElMessage({
        showClose: true,
        message: errorMessage,
        type: "error"
      });
    }
  };

  
  const getOneDockBoat = async (boat_id) => {
    try {
      const response = await axios.get(`/docked/ship/${boat_id}/`);
      if (response.data.code === -1) {
        ElMessage({
          showClose: true,
          message: response.data.message,
          type: "error"
        });
        return;
      } else {
        return response.data.arrive_status; // 返回到港记录数组
      }
    } catch (error) {
      let errorMessage = "请求错误！";
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage += " 详情: " + error.response.data.detail;
      }
      ElMessage({
        showClose: true,
        message: errorMessage,
        type: "error"
      });
    }
  };
  
  const getBoatInfo = async () => {
    try {
      const response = await axios.get("/ships/");
      boatList.value = response.data;
    }
    catch (error) {
      let errorMessage = "请求错误！";
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage += " 详情: " + error.response.data.detail;
      }
      ElMessage({
        showClose: true,
        message: errorMessage,
        type: "error"
      });
    }
  };
  
  const getWeatherInfo = async () => {
    try {
      const response = await axios.get(`/weather/`);
      weatherList.value = response.data;
    }
    catch (error) {
      let errorMessage = "请求错误！";
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage += " 详情: " + error.response.data.detail;
      }
      ElMessage({
        showClose: true,
        message: errorMessage,
        type: "error"
      });
    }
  };
  
  const createWeatherCircles = (weather) => {
    const circles = [
      // 第一个圆：亮黄色，较大的范围
      L.circle([weather.weather_latitude, weather.weather_longitude], {
        color: '#FFEB3B',         // 亮黄色边框
        fillColor: '#FFEB3B',     // 亮黄色填充
        fillOpacity: 0.5,         // 半透明填充
        radius: 15000,            // 增大范围
        stroke: false
      }),
      // 第二个圆：稍深一些的黄色，范围稍小
      L.circle([weather.weather_latitude, weather.weather_longitude], {
        color: '#FFEB3B',         // 亮黄色边框
        fillColor: '#FFEB3B',     // 亮黄色填充
        fillOpacity: 0.5,         // 半透明填充
        radius: 12000,            // 范围稍小
        stroke: false
      }),
      // 第三个圆：深黄色，范围进一步减小
      L.circle([weather.weather_latitude, weather.weather_longitude], {
        color: '#FF9800',         // 深黄色边框
        fillColor: '#FF9800',     // 深黄色填充
        fillOpacity: 0.5,         // 半透明填充
        radius: 10000,            // 范围减小
        stroke: false
      }),
      // 第四个圆：非常深的黄色，最小范围
      L.circle([weather.weather_latitude, weather.weather_longitude], {
        color: '#FF5722',         // 更深的橙黄色
        fillColor: '#FF5722',     // 更深的橙黄色填充
        fillOpacity: 0.5,         // 半透明填充
        radius: 8000,             // 最小范围
        stroke: false
      })
    ];

    // 将所有圆添加到地图，并存入 `weatherCircleList`
    circles.forEach(circle => {
      circle.addTo(map.value);
      weatherCircleList.value.push(circle);
    });
  };

  
  const getOneTrack = async (boat_id) => {
    try {
      const response = await axios.get(`/voyages/ship/${boat_id}/`);
      if (response.data.code === -1) {
        ElMessage({
          showClose: true,
          message: response.data.message,
          type: "error"
        });
        return null;
      } else {
        return response.data.voyages; // 返回航迹记录数组
      }
    } catch (error) {
      let errorMessage = "请求错误！";
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage += " 详情: " + error.response.data.detail;
      }
      ElMessage({
        showClose: true,
        message: errorMessage,
        type: "error"
      });
      return null;
    }
  };
  
  const getOneLog = async (boat_id) => {
    try {
      const response = await axios.get(`/logs/ship/${boat_id}/`);
      if (response.data.code === -1) {
        ElMessage({
          showClose: true,
          message: response.data.message,
          type: "error"
        });
        return null;
      } else {
        return response.data.logs; // 返回日志记录数组
      }
    } catch (error) {
      let errorMessage = "请求错误！";
      if (error.response && error.response.data && error.response.data.message) {
        errorMessage += " 详情: " + error.response.data.message;
      }
      ElMessage({
        showClose: true,
        message: errorMessage,
        type: "error"
      });
      return null;
    }
  };

  
  var BoatIcon = L.icon({
      iconUrl: boatMarkerImage, 
      iconSize: [30, 30], 
      iconAnchor: [15, 30],
      popupAnchor: [1, -34],
  });
  
  var HarborIcon = L.icon({
      iconUrl: harborMarkerImage, 
      iconSize: [30, 30],
      iconAnchor: [15, 30], 
      popupAnchor: [1, -34], 
  });
  
  var WeatherIcon = L.icon({
      iconUrl: weatherMarkerImage, 
      iconSize: [30, 30],
      iconAnchor: [15, 30], 
      popupAnchor: [1, -34], 
  });
  
  var LogIcon = L.icon({
      iconUrl: logMarkerImage, 
      iconSize: [30, 30], 
      iconAnchor: [15, 30], 
      popupAnchor: [1, -34], 
  });
  
  const closeAndRemoveMarkers = (markers, map) => {
    markers.forEach(marker => {
      if (marker.getPopup()) {
        marker.closePopup();
      }
      map.removeLayer(marker);
    });
  };
  
  const closeAndRemoveCircles = (circles, map) => {
    circles.forEach(circle => {
      map.removeLayer(circle);
    });
  };
  
  const formatTime = (cellValue) => {
    if (!cellValue) return '0s';
    const hours = Math.floor(cellValue / 3600);
    const minutes = Math.floor((cellValue % 3600) / 60);
    const seconds = cellValue % 60;
    return `${hours}h ${minutes}m ${seconds}s`;
  };
  
  
  onMounted(async () => {
  
    // 生成地图图层
    map.value = L.map("map", {
      zoomControl: false,
      center: initialCenter.value,
      zoom: 5,
      minZoom: 3,
    });
  
    // 设置地图边界
    const bounds = L.latLngBounds(
      L.latLng(-90, -180), 
      L.latLng(90, 180) 
    );
    map.value.setMaxBounds(bounds);
    map.value.options.maxBoundsViscosity = 1.0;
  
    L.control
      .zoom({
        position: "topright"
      })
      .addTo(map.value);
    
    // 使用高德的WMS服务
    L.tileLayer('http://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
        subdomains: ['1', '2', '3', '4'],
    }).addTo(map.value);

    center.value = initialCenter.value;
  
    /* -------------获得港口信息------------- */
    await getPortInfo()
  
    // 标记港口位置
    harborsMarkerList.value = await Promise.all(harborsList.value.map(async (harbor) => {
      var marker = L.marker([harbor.port_latitude, harbor.port_longitude], { icon: HarborIcon }).addTo(map.value);
      
      // 自定义弹出层内容
      var harborContext = `
        <div class="custom-popup" style="margin:-5pt;">
            <h2 style="font-family: 'STZhongsong'; margin-bottom: -5px;">${harbor.port_name}</h2>
            <p><span style="min-width: 110px; display: inline-block;"><strong>港口编号:</strong> ${harbor.port_id}</span>        &nbsp<span style="min-width: 110px; display: inline-block;"><strong>港口水深:</strong> ${harbor.port_depth == -1 ? '暂无' : harbor.port_depth + ' m'}</span></p>
            <p style="margin-top: -10px;"><span style="min-width: 110px; display: inline-block;"><strong>所处经度:</strong> ${harbor.port_longitude}</span> &nbsp<span style="min-width: 110px; display: inline-block;"><strong>所处纬度:</strong> ${harbor.port_latitude}</span></p>
        </div>
      `;
  
      // 点击时显示港口信息
      marker.bindPopup(harborContext, {
          direction: 'top' // 显示在标记的上方
      });
  
      // 点击事件监听器，详细展示港口信息
      marker.on('click', async function(e) {
        if (e.originalEvent) { // 阻止事件传播
          e.originalEvent.stopPropagation();
        }
        const detailed_harbor = await GetCertainHarbor(harbor);
        harbor = detailed_harbor
        document.getElementById('harbor-name').innerText = harbor.port_name;
        document.getElementById('harbor-id').innerText = harbor.port_id;
        document.getElementById('harbor-country').innerText = harbor.port_country;
        document.getElementById('harbor-year').childNodes[1].nodeValue = ' ' + (harbor.port_build_date == null ? '暂无' : harbor.port_build_date);
        document.getElementById('harbor-depth').childNodes[1].nodeValue = ' ' + (harbor.port_depth == -1 ? '暂无' : harbor.port_depth + ' m');
        document.getElementById('harbor-latitude').childNodes[1].nodeValue = ' ' + (harbor.port_latitude == -1 ? '暂无' : harbor.port_latitude);
        document.getElementById('harbor-longitude').childNodes[1].nodeValue = ' ' + (harbor.port_longitude == -1 ? '暂无' : harbor.port_longitude);
        document.getElementById('harbor-summary').childNodes[1].nodeValue = ' ' + (harbor.port_text == -1 ? '暂无' : harbor.port_text);
        document.querySelector('#harbor-photo img').src = 'http://127.0.0.1:8000' + harbor.port_img;
        document.getElementById('harbors-info').classList.remove('hidden');
        document.getElementById('boat-info').classList.add('hidden');
      });
  
      return marker;
  
    }));
  
    /* -------------获得船舶信息------------- */
    await getBoatInfo();
  
    // 标记船舶位置
    boatMarkerList.value = await Promise.all(boatList.value.map(async (boat) => {
      var boat_marker = L.marker([boat.ship_latitude, boat.ship_longitude], { icon: BoatIcon }).addTo(map.value);
  
      // 自定义弹出层内容
      var boatContext = `
      <div class="custom-popup" style="margin:-5pt;">
          <h2 style="font-family: 'STZhongsong'; margin-bottom: -5px;">${boat.ship_name}</h2>
          <p><span style="min-width: 110px; display: inline-block;"><strong>船舶呼号:</strong> ${boat.ship_id}</span>        &nbsp<span style="min-width: 110px; display: inline-block;"><strong>船舶型号:</strong> ${boat.ship_model == "" ? '暂无' : boat.boat_model}</span></p>
          <p style="margin-top: -10px;"><span style="min-width: 110px; display: inline-block;"><strong>所处经度:</strong> ${boat.ship_longitude}</span> &nbsp<span style="min-width: 110px; display: inline-block;"><strong>所处纬度:</strong> ${boat.ship_latitude}</span></p>
      </div>
      `;
  
      // 点击时显示港口信息
      boat_marker.bindPopup(boatContext, {
          direction: 'top' // 显示在标记的上方
      });
  
      // 点击事件监听器，详细展示船舶信息
      boat_marker.on('click', async function(e) {
        if (e.originalEvent) { // 阻止事件传播
          e.originalEvent.stopPropagation();
        }
        
        document.getElementById('boat-name').innerText = boat.ship_name;
        document.getElementById('boat-id').innerText = boat.ship_id;
        document.getElementById('boat-country').innerText = boat.ship_country;
        document.getElementById('boat-model').childNodes[1].nodeValue = ' ' + (boat.ship_model == "" ? '暂无' : boat.ship_model);
        document.getElementById('boat-weight').childNodes[1].nodeValue = ' ' + (boat.ship_weight == null ? '暂无' : boat.ship_weight + ' 吨');
        document.getElementById('boat-size').childNodes[1].nodeValue = ' ' + (boat.ship_size == null ? '暂无' : boat.ship_size + ' m');
        document.getElementById('boat-status').childNodes[1].nodeValue = ' ' + (boat.ship_status == 1 ? '到港' : '航行');
        document.getElementById('boat-build-date').childNodes[1].nodeValue = ' ' + (boat.ship_build_date == null ? '暂无' : boat.ship_build_date);
        document.getElementById('boat-serve-date').childNodes[1].nodeValue = ' ' + (boat.ship_serve_date == null ? '暂无' : boat.ship_serve_date);
        document.getElementById('boat-longitude').childNodes[1].nodeValue = ' ' + boat.ship_longitude;
        document.getElementById('boat-latitude').childNodes[1].nodeValue = ' ' + boat.ship_latitude;
  
        document.getElementById('boat-info').classList.remove('hidden');
        document.getElementById('harbors-info').classList.add('hidden');
  
        if(boat.ship_status == 1){
          /* -------------获得到港船舶的信息------------- */
          ifArrive.value = true;
          const boat_arrive_status = await getOneDockBoat(boat.ship_id);
          // 更新第一个到港记录的港口名称和到达时间
          if (boat_arrive_status && boat_arrive_status.length > 0) {
            document.getElementById('arrive-harbor').childNodes[1].nodeValue = ' ' + boat_arrive_status[0].port_name;
            document.getElementById('arrive-time').childNodes[1].nodeValue = ' ' + boat_arrive_status[0].arrive_time;
          } else {
            document.getElementById('arrive-harbor').childNodes[1].nodeValue = ' 未知';
            document.getElementById('arrive-time').childNodes[1].nodeValue = ' 未知';
          }
        }
        else{
          /* -------------获得航行船舶的信息------------- */
          ifArrive.value = false;
          const boat_voyage_status = await getOneTrack(boat.ship_id);

          // 如果有航迹记录，更新页面显示第一个航迹信息
          if (boat_voyage_status && boat_voyage_status.length > 0) {
            const firstVoyage = boat_voyage_status[0]; // 获取第一条航迹

            document.getElementById('boat-departure').childNodes[1].nodeValue = ' ' + firstVoyage.departure.port_name;
            document.getElementById('boat-destination').childNodes[1].nodeValue = ' ' + firstVoyage.destination.port_name;
            document.getElementById('boat-voyage-time').childNodes[1].nodeValue = ' '  + firstVoyage.start_time;
          } else {
            // 如果没有航迹记录，显示默认值
            document.getElementById('boat-departure').childNodes[1].nodeValue = ' 未知';
            document.getElementById('boat-destination').childNodes[1].nodeValue = ' 未知';
            document.getElementById('boat-voyage-time').childNodes[1].nodeValue = ' 未知';
          }
  
          // 这里还需要展示出轨迹信息
          if (props.showTrack) { // 不使用监听器，只在这里判断
            const track_logs = await getOneLog(boat.ship_id);

            console.log("Track logs:", track_logs);
            // 提取日志中的坐标点
            const latLngs = track_logs.map(log => [log.ship_latitude, log.ship_longitude]);

            const firstVoyage = boat_voyage_status[0]; // 获取第一条航迹

            // 添加出发港口的坐标
            latLngs.unshift([firstVoyage.departure.port_latitude, firstVoyage.departure.port_longitude]);

            // 添加当前船舶的坐标
            latLngs.push([boat.ship_latitude, boat.ship_longitude]);
            console.log("LatLngs Array:", latLngs);

            if (currentPolyline) {
              map.value.removeLayer(currentPolyline);
              currentPolyline = null;
            }
  
            currentPolyline = L.polyline(latLngs, { color: 'blue' }).addTo(map.value);
            map.value.fitBounds(currentPolyline.getBounds());
  
            // 移除之前的所有标记
            logMarkerList.forEach(marker => {
              map.value.removeLayer(marker);
            });
            logMarkerList = [];
  
            const markers = await Promise.all(track_logs.map(async (log) => {
              var log_marker = L.marker([log.ship_latitude, log.ship_longitude], { icon: LogIcon }).addTo(map.value);
  
              var logContext = `
                <div class="custom-popup" style="margin:-5pt;">
                    <h2 style="font-family: 'STZhongsong'; margin-bottom: -5px;">${log.log_time}</h2>
                    <p><span style="min-width: 110px; display: inline-block;"><strong>船舶速度:</strong> ${log.ship_speed + ' 节'}</span> &nbsp<span style="min-width: 110px; display: inline-block;"><strong>行驶方向:</strong> ${log.ship_direction + ' °'}</span></p>
                    <p style="margin-top: -10px;"><span style="min-width: 110px; display: inline-block;"><strong>所处经度:</strong> ${log.ship_longitude}</span> &nbsp<span style="min-width: 110px; display: inline-block;"><strong>所处纬度:</strong> ${log.ship_latitude}</span></p>
                </div>
              `;
  
              log_marker.bindPopup(logContext, {
                direction: 'top' // 显示在标记的上方
              });
  
              logMarkerList.push(log_marker); // 将标记存储在数组中
              return log_marker;
            }));
  
            const rerenderMarkers = () => {
              // 移除所有标记
              logMarkerList.forEach(marker => {
                map.value.removeLayer(marker);
              });
              // 重新添加标记
              logMarkerList.forEach(marker => {
                marker.addTo(map.value);
              });
            };
  
            // 为地图添加新的点击事件监听器
            map.value.on('click', () => {
              if (currentPolyline) {
                map.value.removeLayer(currentPolyline);
                currentPolyline = null;
              }
              logMarkerList.forEach(marker => {
                marker.closePopup();
                map.value.removeLayer(marker);
              });
              logMarkerList = [];
            });
  
            // 为地图添加缩放和移动事件监听器
            map.value.on('zoomend', rerenderMarkers);
            map.value.on('moveend', rerenderMarkers);
          }
        }
      });
      return boat_marker;
    }));
  
    /* -------------获得天气信息------------- */
    await getWeatherInfo()
  
    // 标记天气位置
    weatherMarkerList.value = await Promise.all(weatherList.value.map(async (weather) => {
      var weather_marker = L.marker([weather.weather_latitude, weather.weather_longitude], { icon: WeatherIcon }).addTo(map.value);
  
      createWeatherCircles(weather);
      
      // 自定义弹出层内容
      var weatherContext = `
        <div class="custom-popup" style="margin:-5pt;">
            <p><span style="min-width: 110px; display: inline-block;"><strong>经度:</strong> ${weather.weather_longitude}</span>        &nbsp<span style="min-width: 110px; display: inline-block;"><strong>纬度:</strong> ${weather.weather_latitude}</span></p>
            <p style="margin-top: -10px;">
              <span style="min-width: 110px; display: inline-block;">
                <strong>海面气温:</strong> ${weather.temperature == -99.9 ? '暂无' : weather.temperature + ' ℃'}
              </span> &nbsp
              <span style="min-width: 110px; display: inline-block;">
                <strong>波浪高度:</strong> ${weather.wave_height == -99.9 ? '暂无' : weather.wave_height + ' m'}
              </span> 
            </p>
            <p style="margin-top: -10px;">
              <span style="min-width: 110px; display: inline-block;">
                <strong>海面风向:</strong> ${weather.wind_direction == -99.9 ? '暂无' : weather.wind_direction + ' °'}
              </span> &nbsp
              <span style="min-width: 110px; display: inline-block;">
                <strong>海面风速:</strong> ${weather.wind_speed == -99.9 ? '暂无' : weather.wind_speed + ' m/s'}
              </span>
            </p>
            <p style="margin-top: -10px;">
              <span style="min-width: 110px; display: inline-block;">
                <strong>海面气压:</strong> ${weather.pressure == -99.9 ? '暂无' : weather.pressure + ' hpa'}
              </span> &nbsp
              <span style="min-width: 110px; display: inline-block;">
                <strong>海水温度:</strong> ${weather.wave_temperature == -99.9 ? '暂无' : weather.wave_temperature + ' ℃'}
              </span>
            </p>
            <p style="margin-top: -10px;">
              <span style="min-width: 110px; display: inline-block;">
                <strong>影响区域:</strong> ${weather.impact_area == -99.9 ? '暂无' : weather.impact_area + ' 平方海里'}
                </span> &nbsp
              <span style="min-width: 110px; display: inline-block;">
                <strong>波浪周期:</strong> ${weather.wave_period == -99.9 ? '暂无' : weather.wave_period + ' s'}
              </span>
            </p>
        </div>
      `;
  
      // 点击时显示港口信息
      weather_marker.bindPopup(weatherContext, {
          direction: 'top' // 显示在标记的上方
      });
  
      return weather_marker;
  
     }));
  
  });
  
  document.addEventListener('click', function(event) {
    const harbor_popup = document.getElementById('harbors-info');
    const boat_popup = document.getElementById('boat-info');
    if (!harbor_popup.contains(event.target)) {
      document.getElementById('harbors-info').classList.add('hidden');
    }
    if (!boat_popup.contains(event.target)) {
      document.getElementById('boat-info').classList.add('hidden');
    }
  });
  
  watch(() => props.latitude, (newVal) => {
    if (map) {
      map.value.setView([newVal, props.longitude], 10);
    }
  });
  
  watch(() => props.longitude, (newVal) => {
    if (map) {
      map.value.setView([props.latitude, newVal], 10);
    }
  });
  
  watch(() => props.ship_latitude, (newVal) => {
    if (map) {
      map.value.setView([newVal, props.ship_longitude], 10);
    }
  });
  
  watch(() => props.ship_longitude, (newVal) => {
    if (map) {
      map.value.setView([props.ship_latitude, newVal], 10);
    }
  });
  
  watch(() => props.showHarbor, (newVal) => {
    if (newVal && map.value) {
      harborsMarkerList.value.forEach(marker => marker.addTo(map.value));
    } else if (map.value) {
      closeAndRemoveMarkers(harborsMarkerList.value, map.value);
    }
  });
  
  watch(() => props.showBoat, (newVal) => {
    if (newVal && map.value) {
      boatMarkerList.value.forEach(marker => marker.addTo(map.value));
    } else if (map.value) {
      closeAndRemoveMarkers(boatMarkerList.value, map.value);
    }
  });
  
  watch(() => props.showWeather, (newVal) => {
    if (newVal && map.value) {
      weatherMarkerList.value.forEach(marker => marker.addTo(map.value));
      weatherCircleList.value.forEach(circle => circle.addTo(map.value));
    } else if (map.value) {
      closeAndRemoveMarkers(weatherMarkerList.value, map.value);
      closeAndRemoveCircles(weatherCircleList.value, map.value);
    }
  });
  
  
  </script>
  
  
  <style scoped>
  #map {
    height: 93.7vh;
    width: 100vw;
  }
  
  .location-bar {
    width: 225px;
    height: 40px;
    position: absolute;
    bottom: 5%;
    left: 10%;
    transform: translate(-50%, 0%);
    z-index: 1000;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    text-align: center;
    font-size: 15px;
    background-color: #8d96bb;  /* 修改按钮底色 */
    color: white;  /* 修改文字颜色 */
    border: none;  /* 去除按钮边框 */
    margin-top: 10px;
  }

  .location-bar:hover {
    background-color: #3e48a4;  /* 鼠标悬浮时的底色 */
  }

  #harbors-info{
    width: 500px;
    min-height: 250px;
    display: flex;
    background: white;
    border-radius: 5px;
    position: absolute;
    right: 60px;
    top: 30px;
    z-index: 9999;
    flex-direction: column;
  }
  
  #harbor-main-info{
    width: 500px;
    height: 175px;
    display: flex;
    /* border: 1px solid black; */
    padding-left: 15px;
  }
  
  #harbor-text-info{
    width: 250px;
    height: 175px;
    /* border: 1px solid black; */
  }
  
  #harbor-photo{
    margin-left: -5px;
    margin-top: 35px;
    width: 200px;
    height: 125px;
    overflow: hidden;
    border-radius: 5px;
    /* border: 1px solid black; */
  }
  
  #harbor-photo img{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  #harbor-name{
    margin-top: 25px;
    width: 250px;
    text-align: center;
    font-family: STZhongsong;
    font-size: 36px;
    /* border: 1px solid black; */
  }
  
  #harbor-id-country{
    margin-top: 10px;
    display: flex
  }
  
  #harbor-id{
    width: 125px;
    font-family: STZhongsong;
    padding-left: 60px;
    /* border: 1px solid black; */
    font-size: 14px;
    color: #999999
  }
  
  #harbor-country{
    width: 125px;
    font-family: STZhongsong;
    text-align: center;
    padding-right: 45px;
    /* border: 1px solid black; */
    font-size: 14px;
    color: #999999
  }
  
  #harbor-year, #harbor-depth, #harbor-latitude, #harbor-longitude{
    min-width: 110px; 
    display: inline-block;
    font-family: STZhongsong;
  }
  
  #harbor-info-detail{
    text-align: center;
  }
  
  #harbor-info-detail p{
    display: inline-block;
    text-align: left;
    margin-left: 10px;
  }
  
  #harbor-summary{
    width: 430px;
    font-family: STZhongsong;
    margin-left: 35px;
    margin-top: 5px;
    margin-bottom: 25px;
  }
  
  #boat-info{
    width: 500px;
    min-height: 250px;
    display: flex;
    background: white;
    border-radius: 5px;
    position: absolute;
    right: 60px;
    top: 30px;
    z-index: 9999;
    flex-direction: column;
  }
  
  #boat-detail{
    text-align: center;
  }
  
  #boat-detail p{
    display: inline-block;
    text-align: left;
  }
  
  #boat-name{
    margin-top: 10px;
    width: 500px;
    height: 60px;
    text-align: center;
    font-family: STZhongsong;
    font-size: 36px;
    /* border: 1px solid black; */
  }
  
  #boat-id-country{
    margin: 0 auto;
    display: flex;
    width: 250px;
    /* border: 1px solid black; */
  }
  
  #boat-id{
    width: 125px;
    font-family: STZhongsong;
    padding-left: 60px;
    /* border: 1px solid black; */
    font-size: 16px;
    color: #999999
  }
  
  #boat-country{
    width: 125px;
    font-family: STZhongsong;
    text-align: center;
    padding-right: 45px;
    /* border: 1px solid black; */
    font-size: 16px;
    color: #999999
  }
  
  #boat-model-weight-size{
    margin-top: 20px;
  }
  
  #boat-status-build-serve{
    margin-top: -20px;
  }
  
  #boat-longitude-latitude{
    margin-top: -20px;
  }
  
  #boat-model, #boat-weight, #boat-size, #boat-status, #boat-build-date, #boat-serve-date,
  #boat-longitude, #boat-latitude, #boat-departure, #boat-destination, #boat-voyage-time{
    min-width: 135px; 
    display: inline-block;
    font-family: STZhongsong;
  }
  
  .hidden {
    display: none !important;
  }
  
  ::v-deep() .el-progress__text {
    font-family: STZhongsong;
    font-weight: bold;
    font-size: 16px !important;
  }
  
  #boat-detail-status{
    margin-top: 10px;
    width: 500px;
    height: 100px;
    /* border: 1px solid black; */
    display: flex;
  }
  
  #boat-detail-status-voyage{
    margin-left: 30px;
  }
  
  #boat-detail-status-text{
    margin-left: 30px;
    margin-top: 5px;
    width: 200px;
    height: 100px;
    /* border: 1px solid black; */
    display: flex;
    flex-direction: column;
    font-family: STZhongsong;
  }
  
  #arrive-harbor, #arrive-time, #leave-time{
    margin-top: 5px;
  }
  
  .dashboard{
    margin-left: 90px;
    width: 100px;
    height: 100px;
    /* border: 1px solid black */
  }
  
  .percentage-value {
    display: block;
  }
  
  .percentage-label{
    margin-top: 10px;
    display: block;
    font-size: 12px;
  }
  
  </style>
  