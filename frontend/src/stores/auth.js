import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const auth_api = axios.create({
  baseURL: '/auth',
  timeout: 4500,
  withCredentials: true,
})

auth_api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        await axios.post('/auth/refresh')
        return auth_api(originalRequest)
      } catch (error) {
        return Promise.reject(error)
      }
    }
    return Promise.reject(error)
  },
)

export const useAuthStore = defineStore('auth', () => {
  //state
  const isAuthorized = localStorage.getItem('isAuthorized') === 'true' ? ref(true) : ref(false)
  const user = ref()
  const devices = ref()

  //functions
  async function login(params) {
    await auth_api.post('/login', params)

    isAuthorized.value = true
    localStorage.setItem('isAuthorized', 'true')

    await getUser()
    await getDevices()

    localStorage.setItem('isAuthorized', true)
  }

  async function logout() {
    await auth_api.post('/logout')
    isAuthorized.value = false
    localStorage.removeItem('isAuthorized')
  }

  async function logoutAll() {
    await auth_api.post('/logout-all')
    isAuthorized.value = false
    localStorage.removeItem('isAuthorized')
  }

  async function getUser() {
    const res = await auth_api.get('/user')
    user.value = res.data
  }

  async function getDevices() {
    const res = await auth_api.get('/devices')
    devices.value = res.data
  }

  return { isAuthorized, user, devices, login, getUser, getDevices, logout, logoutAll }
})
