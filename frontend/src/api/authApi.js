import apiClient from './axios'

export const authApi = {
  login: async (credentials) => {
    const response = await apiClient.post('/api/auth/login', credentials)
    return response.data
  },

  signup: async (userData) => {
    const response = await apiClient.post('/api/auth/signup', userData)
    return response.data
  },

  refreshToken: async () => {
    const response = await apiClient.post('/api/auth/refresh')
    return response.data
  },

  logout: async () => {
    const response = await apiClient.post('/api/auth/logout')
    return response.data
  },

  getProfile: async () => {
    const response = await apiClient.get('/api/auth/profile')
    return response.data
  }
}
