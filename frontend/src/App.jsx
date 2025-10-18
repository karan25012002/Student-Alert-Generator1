import React, { Suspense, lazy } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import useAuthStore from './store/authStore'

// Lazy load page components for better code splitting
const Login = lazy(() => import('./pages/Login'))
const Signup = lazy(() => import('./pages/Signup'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const AcademicPerformance = lazy(() => import('./pages/AcademicPerformance'))
const AttendanceTracking = lazy(() => import('./pages/AttendanceTracking'))
const EngagementInsights = lazy(() => import('./pages/EngagementInsights'))
const Alerts = lazy(() => import('./pages/Alerts'))
const AlertGenerator = lazy(() => import('./pages/AlertGenerator'))
const Layout = lazy(() => import('./components/Layout'))
const ErrorBoundary = lazy(() => import('./components/ErrorBoundary'))

// Loading component for Suspense fallback
const LoadingSpinner = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
)

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

          <Suspense fallback={<LoadingSpinner />}>
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
        </Suspense>
      </div>
    </Router>
    </ErrorBoundary>
  )
}

export default App
