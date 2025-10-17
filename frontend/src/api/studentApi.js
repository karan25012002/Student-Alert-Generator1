import apiClient from './axios'

export const studentApi = {
  getStudentData: async (studentId) => {
    const response = await apiClient.get(`/student/data/${studentId}`)
    return response.data
  },

  getAcademicPerformance: async (studentId) => {
    const response = await apiClient.get(`/student/${studentId}/academic`)
    return response.data
  },

  getAttendanceData: async (studentId) => {
    const response = await apiClient.get(`/student/${studentId}/attendance`)
    return response.data
  },

  getEngagementData: async (studentId) => {
    const response = await apiClient.get(`/student/${studentId}/engagement`)
    return response.data
  },

  getAlerts: async (parentId) => {
    const response = await apiClient.get(`/alerts/${parentId}`)
    return response.data
  },

  markAlertAsRead: async (alertId) => {
    const response = await apiClient.patch(`/alerts/${alertId}/read`)
    return response.data
  },

  getInsights: async (studentId) => {
    const response = await apiClient.get(`/insights/${studentId}`)
    return response.data
  },

  generateInsights: async (studentId, query) => {
    const response = await apiClient.post(`/insights/${studentId}/generate`, { query })
    return response.data
  }
}
