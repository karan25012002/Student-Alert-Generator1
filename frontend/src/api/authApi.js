import apiClient from './axios'

export const authApi = {
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login', credentials)
    return response.data
  },

  signup: async (userData) => {
    const response = await apiClient.post('/auth/signup', userData)
    return response.data
  },

  refreshToken: async () => {
    const response = await apiClient.post('/auth/refresh')
    return response.data
  },

  logout: async () => {
    const response = await apiClient.post('/auth/logout')
    return response.data
  },

  getProfile: async () => {
    const response = await apiClient.get('/auth/profile')
    return response.data
  }
}
