import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5分钟超时
});

export const convertNovel = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/convert', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response;
};

export const getProcessingStatus = async (taskId) => {
  const response = await api.get(`/status/${taskId}`);
  return response.data;
}; 