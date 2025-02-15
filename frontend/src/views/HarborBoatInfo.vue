<template>
    <div v-if="showBoatInfo && boatInfo" id="boat-info">
      <div id="boat-name">{{ boatInfo.ship_name || "暂无" }}</div>
      <div id="boat-id-country">
        <div id="boat-id">{{ boatInfo.ship_id || "暂无" }}</div>
        <div id="boat-country">{{ boatInfo.ship_country || "暂无" }}</div>
      </div>
      <div id="boat-detail">
        <p id="boat-model-weight-size">
          <span id="boat-model"><strong>船舶型号:</strong> {{ boatInfo.ship_model || "暂无" }}</span>
        </p>
      </div>
      <button @click="$emit('close')">关闭</button>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    boatInfo: {
      type: Object,
      default: () => ({}), // 确保默认是一个空对象
    },
    showBoatInfo: {
      type: Boolean,
      default: false, // 默认隐藏
    },
  });
  </script>
  
  <style scoped>
  #boat-info {
    width: 500px;
    min-height: 250px;
    background: white;
    border-radius: 5px;
    position: absolute;
    top: 30px;
    right: 60px;
    z-index: 9999;
    padding: 15px;
  }
  
  #boat-name {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  #boat-id-country {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  #boat-detail {
    margin-top: 10px;
  }
  
  button {
    margin-top: 20px;
    background-color: #3e48a4;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #2c3684;
  }
  </style>
  