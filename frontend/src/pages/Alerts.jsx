import React, { useState, useEffect } from 'react'
import { 
  Bell, 
  AlertTriangle, 
  CheckCircle, 
  XCircle, 
  Info,
  Filter,
  Search,
  MoreVertical,
  Calendar,
  Clock
} from 'lucide-react'
import useStudentStore from '../store/studentStore'
import { studentApi } from '../api/studentApi'
import toast from 'react-hot-toast'

const Alerts = () => {
  const { alerts, setAlerts, markAlertAsRead } = useStudentStore()
  const [filteredAlerts, setFilteredAlerts] = useState([])
  const [filterType, setFilterType] = useState('all')
  const [filterPriority, setFilterPriority] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [showRead, setShowRead] = useState(true)

  useEffect(() => {
    // Mock detailed alerts data
    const mockAlerts = [
      {
        id: 1,
        type: 'warning',
        priority: 'high',
        title: 'Math Performance Decline',
        message: 'Your child\'s math scores have dropped by 12% over the past two weeks. Recent quiz scores: 78%, 72%, 75%. Consider scheduling additional tutoring sessions.',
        date: '2024-10-16T10:30:00Z',
        read: false,
        category: 'academic',
        actionRequired: true,
        suggestions: [
          'Schedule a meeting with the math teacher',
          'Consider hiring a tutor',
          'Review homework completion patterns'
        ]
      },
      {
        id: 2,
        type: 'success',
        priority: 'low',
        title: 'Excellent English Performance',
        message: 'Outstanding work in English class! Your child scored 95% on the recent essay and has maintained consistent A grades throughout the semester.',
        date: '2024-10-15T14:20:00Z',
        read: false,
        category: 'academic',
        actionRequired: false,
        suggestions: []
      },
      {
        id: 3,
        type: 'warning',
        priority: 'medium',
        title: 'Attendance Alert',
        message: 'Attendance has dropped to 89% this month, below the required 95% threshold. Missing classes: Oct 8, Oct 12, Oct 14.',
        date: '2024-10-14T09:15:00Z',
        read: true,
        category: 'attendance',
        actionRequired: true,
        suggestions: [
          'Contact school about missed days',
          'Ensure proper health management',
          'Set up morning routine reminders'
        ]
      },
      {
        id: 4,
        type: 'info',
        priority: 'low',
        title: 'Parent-Teacher Conference Scheduled',
        message: 'Your parent-teacher conference has been scheduled for October 25th at 3:00 PM. Please confirm your attendance.',
        date: '2024-10-13T11:45:00Z',
        read: true,
        category: 'general',
        actionRequired: true,
        suggestions: [
          'Add to calendar',
          'Prepare questions for teachers',
          'Review recent progress reports'
        ]
      },
      {
        id: 5,
        type: 'error',
        priority: 'high',
        title: 'Missing Assignment Alert',
        message: 'Science project deadline passed without submission. This assignment is worth 20% of the final grade. Immediate action required.',
        date: '2024-10-12T16:00:00Z',
        read: false,
        category: 'academic',
        actionRequired: true,
        suggestions: [
          'Contact science teacher immediately',
          'Request extension if possible',
          'Complete and submit as soon as possible'
        ]
      },
      {
        id: 6,
        type: 'info',
        priority: 'medium',
        title: 'Study Group Invitation',
        message: 'Your child has been invited to join the advanced mathematics study group. Sessions are every Tuesday and Thursday after school.',
        date: '2024-10-11T13:30:00Z',
        read: true,
        category: 'engagement',
        actionRequired: false,
        suggestions: [
          'Discuss with your child',
          'Check schedule compatibility',
          'Contact group coordinator'
        ]
      },
      {
        id: 7,
        type: 'warning',
        priority: 'medium',
        title: 'Low Engagement in History',
        message: 'Class participation in History has decreased significantly. Teacher notes indicate minimal interaction during discussions and group activities.',
        date: '2024-10-10T12:15:00Z',
        read: false,
        category: 'engagement',
        actionRequired: true,
        suggestions: [
          'Discuss interest in history topics',
          'Meet with history teacher',
          'Explore engaging history resources'
        ]
      },
      {
        id: 8,
        type: 'success',
        priority: 'low',
        title: 'Perfect Week Attendance',
        message: 'Congratulations! Your child maintained perfect attendance this week and arrived on time every day.',
        date: '2024-10-09T15:45:00Z',
        read: true,
        category: 'attendance',
        actionRequired: false,
        suggestions: []
      }
    ]
    
    setAlerts(mockAlerts)
  }, [])

  useEffect(() => {
    filterAlerts()
  }, [alerts, filterType, filterPriority, searchTerm, showRead])

  const filterAlerts = () => {
    let filtered = alerts

    // Filter by read status
    if (!showRead) {
      filtered = filtered.filter(alert => !alert.read)
    }

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter(alert => alert.category === filterType)
    }

    // Filter by priority
    if (filterPriority !== 'all') {
      filtered = filtered.filter(alert => alert.priority === filterPriority)
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(alert => 
        alert.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        alert.message.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Sort by date (newest first) and priority
    filtered.sort((a, b) => {
      const priorityOrder = { high: 3, medium: 2, low: 1 }
      if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
        return priorityOrder[b.priority] - priorityOrder[a.priority]
      }
      return new Date(b.date) - new Date(a.date)
    })

    setFilteredAlerts(filtered)
  }

  const handleMarkAsRead = async (alertId) => {
    try {
      await studentApi.markAlertAsRead(alertId)
      markAlertAsRead(alertId)
      toast.success('Alert marked as read')
    } catch (error) {
      console.error('Alert update error:', error)
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Failed to update alert'
      toast.error(typeof errorMessage === 'string' ? errorMessage : 'Failed to update alert')
    }
  }

  const getAlertIcon = (type) => {
    switch (type) {
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />
      case 'error':
        return <XCircle className="w-5 h-5 text-red-600" />
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-600" />
      case 'info':
      default:
        return <Info className="w-5 h-5 text-blue-600" />
    }
  }

  const getAlertBorderColor = (type) => {
    switch (type) {
      case 'warning':
        return 'border-l-yellow-500'
      case 'error':
        return 'border-l-red-500'
      case 'success':
        return 'border-l-green-500'
      case 'info':
      default:
        return 'border-l-blue-500'
    }
  }

  const getPriorityBadge = (priority) => {
    const colors = {
      high: 'bg-red-100 text-red-800',
      medium: 'bg-yellow-100 text-yellow-800',
      low: 'bg-green-100 text-green-800'
    }
    
    return (
      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${colors[priority]}`}>
        {priority.charAt(0).toUpperCase() + priority.slice(1)}
      </span>
    )
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
    
    if (diffInHours < 1) return 'Just now'
    if (diffInHours < 24) return `${diffInHours}h ago`
    if (diffInHours < 48) return 'Yesterday'
    return date.toLocaleDateString()
  }

  const unreadCount = alerts.filter(alert => !alert.read).length
  const highPriorityCount = alerts.filter(alert => alert.priority === 'high' && !alert.read).length

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Alerts & Notifications</h1>
          <p className="text-gray-600">
            Stay informed about your child's academic progress and important updates
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Bell className="w-5 h-5 text-gray-600" />
            <span className="text-sm text-gray-600">
              {unreadCount} unread
            </span>
            {highPriorityCount > 0 && (
              <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                {highPriorityCount} urgent
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card text-center">
          <Bell className="w-8 h-8 text-blue-600 mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900">{alerts.length}</p>
          <p className="text-sm text-gray-600">Total Alerts</p>
        </div>
        
        <div className="card text-center">
          <AlertTriangle className="w-8 h-8 text-red-600 mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900">{highPriorityCount}</p>
          <p className="text-sm text-gray-600">High Priority</p>
        </div>
        
        <div className="card text-center">
          <CheckCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900">{alerts.filter(a => a.read).length}</p>
          <p className="text-sm text-gray-600">Resolved</p>
        </div>
        
        <div className="card text-center">
          <Clock className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900">{alerts.filter(a => a.actionRequired && !a.read).length}</p>
          <p className="text-sm text-gray-600">Action Required</p>
        </div>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search alerts..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="input-field"
            >
              <option value="all">All Categories</option>
              <option value="academic">Academic</option>
              <option value="attendance">Attendance</option>
              <option value="engagement">Engagement</option>
              <option value="general">General</option>
            </select>
            
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="input-field"
            >
              <option value="all">All Priorities</option>
              <option value="high">High Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="low">Low Priority</option>
            </select>
            
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={showRead}
                onChange={(e) => setShowRead(e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-600">Show read alerts</span>
            </label>
          </div>
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.length === 0 ? (
          <div className="card text-center py-12">
            <Bell className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No alerts found</h3>
            <p className="text-gray-600">
              {searchTerm || filterType !== 'all' || filterPriority !== 'all' 
                ? 'Try adjusting your filters or search terms.'
                : 'All caught up! No new alerts at the moment.'
              }
            </p>
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <div
              key={alert.id}
              className={`card border-l-4 ${getAlertBorderColor(alert.type)} ${
                alert.read ? 'bg-gray-50' : 'bg-white'
              } hover:shadow-md transition-shadow`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4 flex-1">
                  <div className="flex-shrink-0 mt-1">
                    {getAlertIcon(alert.type)}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className={`text-lg font-semibold ${
                        alert.read ? 'text-gray-600' : 'text-gray-900'
                      }`}>
                        {alert.title}
                      </h3>
                      {getPriorityBadge(alert.priority)}
                      {alert.actionRequired && (
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800">
                          Action Required
                        </span>
                      )}
                      {!alert.read && (
                        <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                      )}
                    </div>
                    
                    <p className={`text-sm mb-3 ${
                      alert.read ? 'text-gray-500' : 'text-gray-700'
                    }`}>
                      {alert.message}
                    </p>
                    
                    {alert.suggestions.length > 0 && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-gray-700 mb-1">Suggested Actions:</p>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {alert.suggestions.map((suggestion, index) => (
                            <li key={index} className="flex items-center space-x-2">
                              <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
                              <span>{suggestion}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <span className="flex items-center space-x-1">
                        <Calendar className="w-3 h-3" />
                        <span>{formatDate(alert.date)}</span>
                      </span>
                      <span className="capitalize">{alert.category}</span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  {!alert.read && (
                    <button
                      onClick={() => handleMarkAsRead(alert.id)}
                      className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                    >
                      Mark as read
                    </button>
                  )}
                  
                  <button className="p-1 text-gray-400 hover:text-gray-600">
                    <MoreVertical className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Quick Actions */}
      {unreadCount > 0 && (
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-blue-900">Quick Actions</h3>
              <p className="text-sm text-blue-700">
                You have {unreadCount} unread alerts that may need your attention.
              </p>
            </div>
            
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  alerts.filter(a => !a.read).forEach(alert => {
                    handleMarkAsRead(alert.id)
                  })
                }}
                className="btn-secondary"
              >
                Mark All as Read
              </button>
              
              <button className="btn-primary">
                View High Priority
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Alerts
