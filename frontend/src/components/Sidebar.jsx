import React from 'react'
import { NavLink } from 'react-router-dom'
import { 
  Home, 
  GraduationCap, 
  Calendar, 
  Activity, 
  Bell,
  Sparkles,
  LogOut,
  User
} from 'lucide-react'
import useAuthStore from '../store/authStore'

const Sidebar = () => {
  const { user, logout } = useAuthStore()

  const navItems = [
    { to: '/dashboard', icon: Home, label: 'Dashboard' },
    { to: '/academic', icon: GraduationCap, label: 'Academic Performance' },
    { to: '/attendance', icon: Calendar, label: 'Attendance' },
    { to: '/engagement', icon: Activity, label: 'Engagement' },
    { to: '/alerts', icon: Bell, label: 'Alerts' },
    { to: '/alert-generator', icon: Sparkles, label: 'Alert Generator' },
  ]

  const handleLogout = () => {
    logout()
  }

  return (
    <div className="bg-white w-64 min-h-screen shadow-lg flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <User className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="font-semibold text-gray-800">{user?.name || 'Parent'}</h2>
            <p className="text-sm text-gray-500">Parent Dashboard</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`
                }
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="p-4 border-t border-gray-200">
        <button
          onClick={handleLogout}
          className="flex items-center space-x-3 px-4 py-3 w-full text-left text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-lg transition-colors"
        >
          <LogOut className="w-5 h-5" />
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </div>
  )
}

export default Sidebar
