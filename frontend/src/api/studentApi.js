import apiClient from './axios'

export const studentApi = {
  getStudentData: async (studentId) => {
    const response = await apiClient.get(`/api/student/data/${studentId}`)
    return response.data
  },

  getAcademicPerformance: async (studentId) => {
    const response = await apiClient.get(`/api/student/${studentId}/academic`)
    return response.data
  },

  getAttendanceData: async (studentId) => {
    const response = await apiClient.get(`/api/student/${studentId}/attendance`)
    return response.data
  },

  getEngagementData: async (studentId) => {
    const response = await apiClient.get(`/api/student/${studentId}/engagement`)
    return response.data
  },

  getAlerts: async (parentId) => {
    const response = await apiClient.get(`/api/alerts/${parentId}`)
    return response.data
  },

  markAlertAsRead: async (alertId) => {
    const response = await apiClient.patch(`/api/alerts/${alertId}/read`)
    return response.data
  },

  getInsights: async (studentId) => {
    const response = await apiClient.get(`/api/insights/${studentId}`)
    return response.data
  },

  generateInsights: async (studentId, query) => {
    const response = await apiClient.post(`/api/insights/${studentId}/generate`, { query })
    return response.data
  }
}
