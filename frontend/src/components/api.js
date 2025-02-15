import axios from "../api/axios"; // 修改为实际的 axios 配置路径
import { ElMessage } from "element-plus";


const GetHarbors = async () => {
  try {
    const response = await axios.get("/ports/");
    harborsList.value = response.data;
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

const GetCertainArriveHarborBoat = async (boat_id) => {
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

const GetAllBoats = async () => {
  try {
    const response = await axios.get("/ships/");
    boatList.value = response.data;
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

const GetAllWeather = async () => {
  try {
    const response = await axios.get(`/weather/`);
    weatherList.value = response.data;
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

const GetCertainTrack = async (boat_id) => {
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

const GetCertainLog = async (boat_id) => {
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

export {
  getLocation,
  GetHarbors,
  GetCertainHarbor,
  GetCertainArriveHarborBoat,
  GetAllBoats,
  GetAllWeather,
  GetCertainTrack,
  GetCertainLog,
};
