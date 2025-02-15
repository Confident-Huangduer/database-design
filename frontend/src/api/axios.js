import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/', // 包含 `/api/` 前缀的完整路径
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 5000,
    withCredentials: true,
});

export default apiClient;
