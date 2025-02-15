<template>
  <div>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :ellipsis="false">
          <span class="navbar-text">船舶轨迹查询系统</span>  <!-- 新增的船舶轨迹查询系统文字 -->
          <div class="flex-grow" />

          <!-- 显示设置独立出来 -->
          <el-sub-menu index="4" class="display-settings-menu">
            <template #title>
              <el-icon><setting /></el-icon>
              <span>地图显示设置</span>
            </template>
            <el-menu-item index="4-1">
              港口位置&nbsp;&nbsp;&nbsp;&nbsp;<el-switch v-model="showHarbor" @click.native.stop="() => {}"/>
            </el-menu-item>
            <el-menu-item index="4-2">
              船舶位置&nbsp;&nbsp;&nbsp;&nbsp;<el-switch v-model="showBoat" @click.native.stop="() => {}"/>
            </el-menu-item>
            <el-menu-item index="4-3">
              船舶轨迹&nbsp;&nbsp;&nbsp;&nbsp;<el-switch v-model="showTrack" @click.native.stop="() => {}"/>
            </el-menu-item>
            <el-menu-item index="4-4">
              水文信息&nbsp;&nbsp;&nbsp;&nbsp;<el-switch v-model="showWeather" @click.native.stop="() => {}"/>
            </el-menu-item>
          </el-sub-menu>

          <!-- 右侧菜单 -->
          <el-menu-item index="1" style="font-size: 14px;">控制台</el-menu-item>
          <el-menu-item index="2" style="font-size: 14px;">欢迎您, 123</el-menu-item>
      </el-menu>

      <el-menu
          default-active="1"
          class="el-menu-vertical-demo"
          :collapse="false"
          @mouseenter="mouseEnter"
          @mouseleave="mouseLeave"
          style="border-radius: 15px; box-shadow: 0 0 5px rgba(0, 0, 0, 0.3); position: absolute; top: 10%; left: 3%; padding-top: 10px; padding-bottom: 10px; z-index: 1000; height: 200px; width: 160px;"
      >
          <el-menu-item index="1" @click="showAllHarbor">
              <el-icon><Place /></el-icon>
              <template #title>港口信息查询</template>
          </el-menu-item>
          <el-menu-item index="2" @click="showAllBoat">
              <el-icon><Ship /></el-icon>
              <template #title>船舶信息查询</template>
          </el-menu-item>
          <el-menu-item index="3" @click="showAllTrack">
              <el-icon><Operation/></el-icon>
              <template #title>船舶轨迹信息</template>
          </el-menu-item>
      </el-menu>
      
      <el-drawer
          v-model="table"
          direction="btt"
          title="港口信息查询"
          size="45%" 
          style="z-index: 1000; text-align: center;"
      >
        <div style="margin: 0 auto; padding: 20px;">
          <el-table :data="harborData" style="width: 38%; margin: 0 auto; table-layout: fixed;">
          <el-table-column property="port_id" label="编号" width="80" header-align="center" align="center" />
          <el-table-column property="port_name" label="名称" width="100" header-align="center" align="center" />
          <el-table-column property="port_country" label="国家" width="80" header-align="center" align="center" />
          <el-table-column property="port_latitude" label="经度" width="80" header-align="center" align="center" />
          <el-table-column property="port_longitude" label="纬度" width="80" header-align="center" align="center" />

          <el-table-column label="船舶信息查询" width="80" header-align="center" align="center" >
              <template v-slot="scope">
                  <div class="icon-container" style="display: flex; justify-content: center; align-items: center;">
                      <el-button
                      type="text"
                      class="center-icon-button"
                      @click="getHarborBoats(scope.row.port_id)"
                      style="padding: 0; margin: 0;"
                      >
                      <el-icon><Ship /></el-icon>
                      </el-button>
                  </div>
              </template>
          </el-table-column>
          <el-drawer
              v-model="innerDrawer"
              title="到港船舶"
              :append-to-body="true"
              size="45%" 
              id="in-harbor-boat"
          >
              <el-table :data="harborBoatData">
                  <el-table-column property="ship_id" label="呼号" width="80" header-align="center" align="center" />
                  <el-table-column property="ship_name" label="名称" width="120" header-align="center" align="center" />
                  <el-table-column property="ship_model" label="型号" width="120" header-align="center" align="center" />
                  <el-table-column property="ship_country" label="国家" width="80" header-align="center" align="center" />
                  <el-table-column property="ship_latitude" label="经度" width="80" header-align="center" align="center" />
                  <el-table-column property="ship_longitude" label="纬度" width="80" header-align="center" align="center" />
                  <el-table-column property="ship_status" label="状态" width="80" :formatter="shipStatus"/>
                  <el-table-column label="" width="80">
                      <template v-slot="scope">
                          <el-button
                              type="text"
                              @click="FindBoatInMap(scope.row.ship_latitude, scope.row.ship_longitude)">
                              <el-icon><location /></el-icon>
                          </el-button>
                      </template>
                  </el-table-column>
              </el-table>
          </el-drawer>

          <el-table-column label="" width="80">
              <template v-slot="scope">
                  <el-button
                      type="text"
                      @click="locateOnMap(scope.row.port_latitude, scope.row.port_longitude)"
                  >
                      <el-icon><location /></el-icon>
                  </el-button>
              </template>
          </el-table-column>
          </el-table>
        </div>
      </el-drawer>

      <el-drawer
          v-model="boat_table"
          direction="btt"
          title="船舶信息查询"
          size="45%"
          style="z-index: 1000; text-align: center;"
      >
        <div style="margin: 0 auto; padding: 20px;">
          <el-table :data="boatData" style="width: 48%; margin: 0 auto; table-layout: fixed;">
              <el-table-column property="ship_id" label="呼号" width="80" />
              <el-table-column property="ship_name" label="名称" width="120" />
              <el-table-column property="ship_model" label="型号" width="120" />
              <el-table-column property="ship_country" label="国家" width="80"/>
              <el-table-column property="ship_latitude" label="经度" width="80"/>
              <el-table-column property="ship_longitude" label="纬度" width="80"/>
              <el-table-column property="ship_status" label="状态" width="80" :formatter="shipStatus">
              </el-table-column>
              <el-table-column label="" width="80">
                  <template v-slot="scope">
                      <el-button
                          type="text"
                          @click="FindBoatInMap(scope.row.ship_latitude, scope.row.ship_longitude)">
                          <el-icon><location /></el-icon>
                      </el-button>
                  </template>
              </el-table-column>
          </el-table>
        </div>
      </el-drawer>

      <el-drawer
          v-model="track_table"
          direction="btt"
          title="船舶轨迹"
          size="45%"
          style="z-index: 1000; text-align: center;"
      >
        <div style="margin: 0 auto; padding: 20px;">
          <el-table :data="trackData" style="width: 57%; margin: 0 auto; table-layout: fixed;">
              <el-table-column property="ship_id" label="呼号" width="80" />
              <el-table-column property="ship_name" label="名称" width="80" />
              <el-table-column property="ship_model" label="型号" width="120" />
              <el-table-column property="ship_latitude" label="经度" width="80"/>
              <el-table-column property="ship_longitude" label="纬度" width="80"/>
              <el-table-column property="start_time" label="出发时间" width="120"/>
              <el-table-column property="departure.port_name" label="出发地" width="120"/>
              <el-table-column property="destination.port_name" label="目的地" width="120"/>
              <el-table-column label="" width="80">
                  <template v-slot="scope">
                      <el-button
                          type="text"
                          @click="FindBoatInMap(scope.row.ship_latitude, scope.row.ship_longitude)">
                          <el-icon><location /></el-icon>
                      </el-button>
                  </template>
              </el-table-column>
          </el-table>
        </div>
      </el-drawer>
      <Map :latitude="latitude" :longitude="longitude" :showHarbor="showHarbor" :showBoat="showBoat" :showTrack="showTrack" :showWeather="showWeather"
           :ship_latitude="ship_latitude" :ship_longitude="ship_longitude"></Map>
  </div>
</template>



<script setup>
import { ref } from "vue";
import Map from "@/views/Map.vue";
import {
Document,
Menu as IconMenu,
Location,
Operation,
Place,
Setting,
Ship,
} from "@element-plus/icons-vue";
import { ElDrawer, ElMessage } from 'element-plus'
import axios from "../api/axios"; // 修改为实际的 axios 配置路径

const props = defineProps({
user: Object
});

const user = ref(props.user);
const activeIndex = ref("1");
const isCollapse = ref(true);
const table = ref(false);
const innerDrawer = ref(false);
const boat_table = ref(false)
const track_table = ref(false)
const harborData = ref([]);
const boatData = ref([]);
const harborBoatData = ref([]);
const trackData = ref([])
const latitude = ref(116.23);
const longitude = ref(39.54);
const ship_latitude = ref(116.23);
const ship_longitude = ref(39.54);

const showHarbor = ref(true);
const showBoat = ref(true);
const showTrack = ref(true);
const showWeather = ref(true);

const formatTime = (row, column, cellValue) => {
  if (!cellValue) return '0s';
  const hours = Math.floor(cellValue / 3600);
  const minutes = Math.floor((cellValue % 3600) / 60);
  const seconds = cellValue % 60;
  return `${hours}h ${minutes}m ${seconds}s`;
};


const mouseEnter = () => {
  isCollapse.value = false
}

const mouseLeave = () => {
  isCollapse.value = true
}

// 获取所有的港口信息查询
const GetHarbors = async () => { 
try {
  const response = await axios.get("/ports/");
  harborData.value = response.data; // 保存获取的数据
}
catch (error) {
  let errorMessage = "请求错误！";
  if (error.response && error.response.data && error.response.data.detail) {
      errorMessage = error.response.data.detail;
  }
  ElMessage({
    showClose: true,
    message: errorMessage,
    type: "error"
  });
}
};

const GetBoats = async () => {
try {
  const response = await axios.get("/ships/");
  boatData.value = response.data;
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

const GetCertainHarborBoat = async (port_id) => {
  try {
    const response = await axios.get(`/docked/port/${port_id}/`);
    if (response.data.code === -1) {
      ElMessage({
        showClose: true,
        message: "船舶信息查询失败！",
        type: "error"
      });
      return;
    } else {
      harborBoatData.value = response.data.data; // 使用后端返回的 "data" 字段
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

const GetAllTrack = async () => {
try {
  const response = await axios.get("/voyages/");
  trackData.value = response.data.data
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

const showAllHarbor = async () => {
  await GetHarbors();
  table.value = true;
}

const showAllBoat = async () => {
  await GetBoats();
  boat_table.value = true;
}

const showAllTrack = async () => {
  await GetAllTrack();
  track_table.value = true;
}

const locateOnMap = (port_latitude, port_longitude) => {
  latitude.value = port_latitude;
  longitude.value = port_longitude;
}

const FindBoatInMap = (port_latitude, port_longitude) => {
  ship_latitude.value = port_latitude;
  ship_longitude.value = port_longitude;
}

const getHarborBoats = async (port_id) => {
  await GetCertainHarborBoat(port_id);
  innerDrawer.value=true;
  
}

const shipStatus = (row, column, cellValue, index) => {
  const statusMap = {
      1: '到港',
      2: '航行'
  };
  return statusMap[cellValue] || '未知';
}

</script>

<style scoped>

  .el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 200px;
  --bg-color: #0793f7 !important;
  }
  .el-menu-demo {
  --bg-color: #0391f7 !important;
  }
  .flex-grow {
  flex-grow: 1;
  }
  /* 默认字体颜色 */
  .el-menu-item {
    color: #333; /* 默认字体颜色 */
    font-size: 14px;
    transition: color 0.3s ease; /* 添加平滑过渡 */
  }

  /* 鼠标悬停时字体变色 */
  .el-menu-item:hover {
    color: #409EFF; /* 颜色与控制台字样一致 */
  }
  /* 修改导航栏文字部分样式 */
  .navbar-text {
    font-size: 28px;
    color: #0061b3; /* 深蓝色文字 */
    font-weight: bolder;
    position: absolute;
    top: 10px;
    left: 110px;
  }

  .harbor-info-titie{
    font-family: STZhongsong;
    font-size: 30px;
    margin-top: -50px;
  }

  ::v-deep() .el-drawer__title{
    font-family: STZhongsong !important;
    font-size: 30px !important;
  }

  ::v-deep() .el-drawer__header{
    margin-bottom: 0px  !important;
  }

  ::v-deep(#in-harbor-boat) .el-drawer__title {
  font-family: 'STZhongsong' !important;
  font-size: 30px !important;
  }

  ::v-deep(#in-harbor-boat) .el-drawer__header{
    margin-bottom: 0px  !important;
  }

  .icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  }

  /* 添加一些样式来调整布局 */
  .display-settings-menu {
    margin-right: 20px; /* 控制左侧“显示设置”与控制台的间距 */
  }

/* 调整弹出框的整体样式 */
.el-drawer {
  font-family: 'Arial', sans-serif; /* 修改字体 */
  color: #333; /* 默认字体颜色 */
  background-color: #f9f9f9; /* 背景颜色 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
  border-radius: 10px; /* 圆角 */
  transition: all 0.3s ease; /* 平滑动画 */
}

  /* 表格标题样式 */
  .el-table th {
    background-color: #197ee3; /* 修改表头背景色 */
    color: #fff; /* 表头文字颜色 */
    font-size: 16px; /* 表头字体大小 */
    text-align: center; /* 居中对齐 */
    font-weight: bold; /* 加粗 */
  }

/* 表格行的默认样式 */
.el-table td {
  color: #1bb2d4c6; /* 表格字体颜色 */
  font-size: 14px; /* 表格字体大小 */
  text-align: center; /* 居中对齐 */
  padding: 10px; /* 行内间距 */
}

/* 鼠标悬停在行上时的高亮效果 */
.el-table .el-table__row:hover td {
  background-color: #f0f7ff; /* 行的高亮背景色 */
  color: #333; /* 行的字体颜色 */
}

/* 按钮的样式 */
.el-button {
  color: #fff;
  background-color: #409EFF; /* 按钮背景色 */
  border-radius: 5px; /* 圆角按钮 */
  transition: all 0.3s ease;
}

/* 按钮悬停样式 */
.el-button:hover {
  background-color: #66b1ff; /* 悬停时背景色 */
  color: #fff; /* 字体颜色保持不变 */
}
</style>
