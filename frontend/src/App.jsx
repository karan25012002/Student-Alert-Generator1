import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import useAuthStore from './store/authStore'

import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import AcademicPerformance from './pages/AcademicPerformance'
import AttendanceTracking from './pages/AttendanceTracking'
import EngagementInsights from './pages/EngagementInsights'
import Alerts from './pages/Alerts'
import AlertGenerator from './pages/AlertGenerator'
import Layout from './components/Layout'
import ErrorBoundary from './components/ErrorBoundary'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
          
          <Routes>
          <Route 
            path="/login" 
            element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" />} 
          />
          <Route 
            path="/signup" 
            element={!isAuthenticated ? <Signup /> : <Navigate to="/dashboard" />} 
          />
          
          <Route 
            path="/" 
            element={isAuthenticated ? <Layout /> : <Navigate to="/login" />}
          >
            <Route index element={<Navigate to="/dashboard" />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="academic" element={<AcademicPerformance />} />
            <Route path="attendance" element={<AttendanceTracking />} />
            <Route path="engagement" element={<EngagementInsights />} />
            <Route path="alerts" element={<Alerts />} />
            <Route path="alert-generator" element={<AlertGenerator />} />
          </Route>
          
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
    </ErrorBoundary>
  )
}

export default App
