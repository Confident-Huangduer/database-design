<template>
  <div class="auth-page">
    <!-- 背景图片 -->
    <div class="background-carousel">
      <div
        class="carousel-slide"
        v-for="(bgImage, idx) in backgroundImages"
        :key="idx"
        :style="{ backgroundImage: 'url(' + bgImage + ')', opacity: idx === activeImageIndex ? 1 : 0 }"
      ></div>
    </div>

    <!-- 中间区域 -->
    <div class="center-container">
      <!-- 左侧欢迎部分 -->
      <div class="welcome-section">
        <h1 class="welcome-title">欢迎注册</h1>
        <br>
        <br>
        <h2 class="welcome-system-name">全球性船舶轨迹查询<br>与信息集成管理系统</h2>
      </div>
      <!-- 右侧注册表单 -->
      <div class="form-container">
        <h2 class="form-header">用户注册</h2>
        <div class="form-divider"></div>
        <form @submit.prevent="handleRegister">
          <input
            type="text"
            v-model="registerUsername"
            class="form-input"
            placeholder="用户名 (小于20位)"
            required
          />
          <input
            type="email"
            v-model="registerEmail"
            class="form-input"
            placeholder="邮箱"
            required
          />
          <input
            type="password"
            v-model="registerPassword"
            class="form-input"
            placeholder="密码 (8-20位)"
            required
          />
          <input
            type="password"
            v-model="registerPasswordConfirm"
            class="form-input"
            placeholder="确认密码"
            required
          />
          <button type="submit" class="form-submit-btn">注册</button>
        </form>
        <p class="form-switch">
          已有账户？
          <router-link to="/login" class="switch-link">返回登录</router-link>
        </p>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router"; // 引入 Vue Router
import axios from "../api/axios"; // 修改为实际的 axios 配置路径
import image1 from "@/static/backimage1.jpg";
import image2 from "@/static/backimage2.jpg";
import image3 from "@/static/backimage3.jpg";

// 背景图片数据
const backgroundImages = [image1, image2, image3];
const activeImageIndex = ref(0);

const router = useRouter(); // 获取路由实例

// 表单数据
const registerUsername = ref("");
const registerEmail = ref("");
const registerPassword = ref("");
const registerPasswordConfirm = ref("");

// 错误信息
const errorMessage = ref("");

// 背景轮播逻辑
const rotateBackground = () => {
  activeImageIndex.value = (activeImageIndex.value + 1) % backgroundImages.length;
};

// 注册逻辑
const handleRegister = async () => {
  if (registerUsername.value.length < 1 || registerUsername.value.length > 20) {
    errorMessage.value = "用户名长度非法！";
    return;
  }

  if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(registerEmail.value)) {
    errorMessage.value = "邮箱格式不正确！";
    return;
  }

  if (registerPassword.value.length < 8 || registerPassword.value.length > 20) {
    errorMessage.value = "密码长度应在8到20位之间！";
    return;
  }

  if (registerPassword.value !== registerPasswordConfirm.value) {
    errorMessage.value = "两次输入的密码不一致！";
    return;
  }

  try {
    const res = await axios.post("/register/", {
      user_name: registerUsername.value,
      user_email: registerEmail.value,
      user_password: registerPassword.value,
    });
    if (res.data.code === 1) {
      alert("注册成功！");
      router.push("/login");
    } else {
      errorMessage.value = res.data.message || "注册失败！";
    }
  } catch (err) {
    errorMessage.value = "网络错误，请稍后再试！";
  }
};

// 自动轮播背景
onMounted(() => {
  setInterval(rotateBackground, 5000);
});
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  overflow: hidden; /* 避免滚动条 */
  width: 100%; /* 确保占满屏幕宽度 */
  height: 100%; /* 确保占满屏幕高度 */
}

.auth-page {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.background-carousel {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw; /* 强制占满窗口宽度 */
  height: 100vh; /* 强制占满窗口高度 */
  z-index: -1;
  overflow: hidden; /* 避免多余内容溢出 */
}

.carousel-slide {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%; /* 背景强制适配父容器宽度 */
  height: 100%; /* 背景强制适配父容器高度 */
  background-size: 100% 100%; /* 拉伸背景以完全覆盖容器 */
  background-position: center; /* 背景居中 */
  background-repeat: no-repeat; /* 不重复背景 */
  transition: opacity 1.5s ease-in-out; /* 背景渐变切换效果 */
}

.center-container {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 60%;
  height: 60%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: row;
  border-radius: 20px; /* 圆角效果 */
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 美化 */
}

.welcome-section {
  flex: 1;
  background-color: rgba(97, 71, 150, 0.899); /* 蓝色半透明背景 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  padding: 20px;
  border-top-left-radius: 20px; /* 左侧圆角 */
  border-bottom-left-radius: 20px;
}

.welcome-title {
  font-size: 40px;
  font-weight: bolder;
  margin-bottom: 10px;
  color: rgb(162, 217, 247);
}

.welcome-system-name {
  font-size: 24px;
  font-weight: bold;
}

.form-container {
  flex: 1;
  padding: 20px;
  background: rgba(248, 244, 243, 0.871);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-top-right-radius: 20px; /* 右侧圆角 */
  border-bottom-right-radius: 20px;
}

.form-header {
  font-size: 24px;
  color: rgb(78, 128, 152);
  margin-bottom: 20px;
  text-align: center;
}

.form-divider {
  width: 80px;
  height: 3px;
  background-color: #4e8098;
  margin: 0 auto 20px;
}

.form-input {
  width: 95%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.form-input:focus {
  outline: none;
  border-color: #4e8098;
  box-shadow: 0 0 3px #4e8098;
}

.form-submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #4e8098;
  color: white;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.form-submit-btn:hover {
  background-color: #3a6874;
}

.form-switch {
  margin-top: 10px;
  text-align: center;
}

.switch-link {
  color: #4e8098;
  text-decoration: underline;
  cursor: pointer;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}
</style>
