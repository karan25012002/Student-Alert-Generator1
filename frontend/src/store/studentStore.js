import { create } from 'zustand'

const useStudentStore = create((set, get) => ({
  studentData: null,
  academicData: null,
  attendanceData: null,
  engagementData: null,
  alerts: [],
  insights: [],
  loading: false,
  error: null,

  setStudentData: (data) => set({ studentData: data }),
  setAcademicData: (data) => set({ academicData: data }),
  setAttendanceData: (data) => set({ attendanceData: data }),
  setEngagementData: (data) => set({ engagementData: data }),
  setAlerts: (alerts) => set({ alerts }),
  setInsights: (insights) => set({ insights }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  addAlert: (alert) => set((state) => ({
    alerts: [alert, ...state.alerts]
  })),

  markAlertAsRead: (alertId) => set((state) => ({
    alerts: state.alerts.map(alert =>
      alert.id === alertId ? { ...alert, read: true } : alert
    )
  })),

  clearError: () => set({ error: null }),
}))

export default useStudentStore
