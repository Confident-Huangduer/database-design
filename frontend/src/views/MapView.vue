<template>
    <div id="map" @mousemove="getLocation">
      <el-button type="primary" class="location-bar">
        经度: {{ formatLatLng(center)[1] }}&nbsp;&nbsp;&nbsp;&nbsp;纬度: {{ formatLatLng(center)[0] }}
      </el-button>
      <HarborBoatInfo
        :harborInfo="harborInfo"
        :boatInfo="boatInfo"
        :showHarborInfo="showHarborInfo"
        :showBoatInfo="showBoatInfo"
        :ifArrive="ifArrive"
        @close="closeInfo"
      />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from "vue";
  import { ElMessage } from "element-plus";
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";
  import axios from "../api/axios";
  import HarborBoatInfo from "./HarborBoatInfo.vue";
  
  import boatMarkerImage from "@/static/boat_icon.png";
  import harborMarkerImage from "@/static/port_icon.png";
  import weatherMarkerImage from "@/static/weather_icon.png";
  import logMarkerImage from "@/static/log_icon.png";
  
  const props = defineProps([
    "latitude",
    "longitude",
    "ship_latitude",
    "ship_longitude",
    "showHarbor",
    "showBoat",
    "showTrack",
    "showWeather",
  ]);
  
  const center = ref([39.54, 116.23]);
  const initialCenter = ref([39.54, 116.23]);
  const map = ref(null);
  const harborsList = ref([]);
  const boatList = ref([]);
  const ifArrive = ref(false);
  
  const harborInfo = ref(null);
  const boatInfo = ref(null);
  const showHarborInfo = ref(false);
  const showBoatInfo = ref(false);
  
  const formatLatLng = (latLng) => latLng.map((coord) => coord.toFixed(3));
  
  const getLocation = (event) => {
    if (map.value) {
      const latlng = map.value.mouseEventToLatLng(event);
      center.value = [latlng.lat, latlng.lng];
      while (center.value[1] < -180) center.value[1] += 360;
      while (center.value[1] > 180) center.value[1] -= 360;
    }
  };
  
  const getPortInfo = async () => {
    try {
      const response = await axios.get("/ports/");
      harborsList.value = response.data;
    } catch (error) {
      handleError(error, "港口信息获取失败");
    }
  };
  
  const getBoatInfo = async () => {
    try {
      const response = await axios.get("/ships/");
      boatList.value = response.data;
    } catch (error) {
      handleError(error, "船舶信息获取失败");
    }
  };
  
  const handleError = (error, message) => {
    let errorMessage = `${message}！`;
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage += `详情: ${error.response.data.detail}`;
    }
    ElMessage({
      showClose: true,
      message: errorMessage,
      type: "error",
    });
  };
  
  const showHarborDetails = (harbor) => {
    harborInfo.value = harbor;
    showHarborInfo.value = true;
    showBoatInfo.value = false;
  };
  
  const showBoatDetails = (boat) => {
    boatInfo.value = boat;
    showHarborInfo.value = false;
    showBoatInfo.value = true;
  };
  
  const closeInfo = () => {
    showHarborInfo.value = false;
    showBoatInfo.value = false;
  };
  
  onMounted(async () => {
    map.value = L.map("map", {
      zoomControl: false,
      center: initialCenter.value,
      zoom: 5,
      minZoom: 3,
    });
  
    L.tileLayer(
      "http://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
      {
        subdomains: ["1", "2", "3", "4"],
      }
    ).addTo(map.value);
  
    await getPortInfo();
    await getBoatInfo();
  
    harborsList.value.forEach((harbor) => {
      const marker = L.marker([harbor.port_latitude, harbor.port_longitude], {
        icon: L.icon({
          iconUrl: harborMarkerImage,
          iconSize: [30, 30],
        }),
      }).addTo(map.value);
  
      marker.on("click", () => showHarborDetails(harbor));
    });
  
    boatList.value.forEach((boat) => {
      const marker = L.marker([boat.ship_latitude, boat.ship_longitude], {
        icon: L.icon({
          iconUrl: boatMarkerImage,
          iconSize: [30, 30],
        }),
      }).addTo(map.value);
  
      marker.on("click", () => showBoatDetails(boat));
    });
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
    z-index: 1000;
    text-align: center;
    background-color: #8d96bb;
    color: white;
    border: none;
    margin-top: 10px;
  }
  
  .location-bar:hover {
    background-color: #3e48a4;
  }
  </style>
  