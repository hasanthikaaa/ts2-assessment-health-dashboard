import axios from "axios";
import type { AxiosResponse, AxiosError } from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// TODO: Q5(b) - Implement error interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    return Promise.reject(error);
  }
);
