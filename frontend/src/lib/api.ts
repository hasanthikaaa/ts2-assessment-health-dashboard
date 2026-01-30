import axios from "axios";
import type { AxiosResponse, AxiosError } from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Error interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    let message = "An unexpected error occurred";

    if (error.response?.data) {
      const data = error.response.data as any;

      if (typeof data.detail === "string") {
        message = data.detail;
      } else if (typeof data.message === "string") {
        message = data.message;
      }
    } else if (error.message) {
      message = error.message;
    }

    return Promise.reject(new Error(message));
  },
);
