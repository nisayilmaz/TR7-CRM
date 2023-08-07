import axios from 'axios';
let isDev = import.meta.env.DEV
const serverUrl = isDev ? "http://localhost:5000" : ""
export const axiosInstance = axios.create({
    baseURL : serverUrl + "/api",
    headers: {
        Authorization : `${localStorage.getItem("accessToken")}`
    }
})

export function updateAuth() {
    axiosInstance.defaults.headers.Authorization = `${localStorage.getItem("accessToken")}`
}

export const noAuthAxiosInstance = axios.create({
    baseURL : serverUrl + "/api"
})

