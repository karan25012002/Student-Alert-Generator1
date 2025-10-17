import React, { useState, useEffect } from 'react'
import { 
  AlertCircle, 
  User, 
  Hash, 
  Calendar, 
  TrendingUp, 
  MessageSquare, 
  Users, 
  FileText,
  Sparkles,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Info,
  Loader,
  Save,
  RefreshCw
} from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'
import useStudentStore from '../store/studentStore'
import useAuthStore from '../store/authStore'

const AlertGenerator = () => {
  const { user } = useStudentStore()
  const { token } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [generatedAlerts, setGeneratedAlerts] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    roll_number: '',
    attendance_percentage: '',
    academic_performance: '',
    behavior_notes: '',
    participation_level: 'medium',
    additional_comments: ''
  })

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const validateForm = () => {
    if (!formData.name.trim()) {
      toast.error('Please enter student name')
      return false
    }
    if (!formData.roll_number.trim()) {
      toast.error('Please enter roll number')
      return false
    }
    if (!formData.attendance_percentage || formData.attendance_percentage < 0 || formData.attendance_percentage > 100) {
      toast.error('Please enter valid attendance percentage (0-100)')
      return false
    }
    if (!formData.academic_performance || formData.academic_performance < 0) {
      toast.error('Please enter valid academic performance')
      return false
    }
    return true
  }

  const handleGenerateAlerts = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return
    
    if (!token) {
      toast.error('Please login to generate alerts')
      // Redirect to login page if not authenticated
      window.location.href = '/login'
      return
    }

    setLoading(true)
    
    try {
      const response = await axios.post(
        'http://localhost:8000/api/alert-generator/generate',
        {
          name: formData.name,
          roll_number: formData.roll_number,
          attendance_percentage: parseFloat(formData.attendance_percentage),
          academic_performance: parseFloat(formData.academic_performance),
          behavior_notes: formData.behavior_notes,
          participation_level: formData.participation_level,
          additional_comments: formData.additional_comments
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          timeout: 10000 // Add timeout
        }
      )

      setGeneratedAlerts(response.data)
      toast.success(`Generated ${response.data.alerts.length} alerts successfully!`)
      
    } catch (error) {
      console.error('Error generating alerts:', error)
      
      // Handle different error types
      if (error.response?.status === 401) {
        toast.error('Authentication expired. Please login again.')
        // Clear auth state and redirect to login
        useAuthStore.getState().logout()
        window.location.href = '/login'
      } else {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to generate alerts'
        toast.error(errorMessage)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSaveAlerts = async () => {
    if (!generatedAlerts || !generatedAlerts.alerts.length) {
      toast.error('No alerts to save')
      return
    }
    
    if (!token) {
      toast.error('Please login to save alerts')
      // Redirect to login page if not authenticated
      window.location.href = '/login'
      return
    }

    setLoading(true)

    try {
      // Use a default student ID - in production, this should come from actual student data
      const studentId = 'STU001'
      
      const response = await axios.post(
        `http://localhost:8000/api/alert-generator/generate-and-save?student_id=${studentId}`,
        {
          name: formData.name,
          roll_number: formData.roll_number,
          attendance_percentage: parseFloat(formData.attendance_percentage),
          academic_performance: parseFloat(formData.academic_performance),
          behavior_notes: formData.behavior_notes,
          participation_level: formData.participation_level,
          additional_comments: formData.additional_comments
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          timeout: 10000 // Add timeout
        }
      )

      toast.success('Alerts saved to dashboard successfully!')
      
      // Reset form after successful save
      setTimeout(() => {
        handleReset()
      }, 1500)
      
    } catch (error) {
      console.error('Error saving alerts:', error)
      
      // Handle different error types
      if (error.response?.status === 401) {
        toast.error('Authentication expired. Please login again.')
        // Clear auth state and redirect to login
        useAuthStore.getState().logout()
        window.location.href = '/login'
      } else {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to save alerts'
        toast.error(errorMessage)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFormData({
      name: '',
      roll_number: '',
      attendance_percentage: '',
      academic_performance: '',
      behavior_notes: '',
      participation_level: 'medium',
      additional_comments: ''
    })
    setGeneratedAlerts(null)
  }

  const getAlertIcon = (type) => {
    switch (type) {
      case 'warning':
        return <AlertTriangle className="w-6 h-6 text-yellow-600" />
      case 'error':
        return <XCircle className="w-6 h-6 text-red-600" />
      case 'success':
        return <CheckCircle className="w-6 h-6 text-green-600" />
      case 'info':
      default:
        return <Info className="w-6 h-6 text-blue-600" />
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
      <span className={`inline-flex px-3 py-1 text-xs font-semibold rounded-full ${colors[priority]}`}>
        {priority.toUpperCase()}
      </span>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-purple-600" />
            Student Alert Generator
          </h1>
          <p className="text-gray-600 mt-2">
            AI-powered analysis to generate intelligent alerts and recommendations
          </p>
        </div>
      </div>

      {/* Info Banner */}
      <div className="card bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            <Sparkles className="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-purple-900 mb-1">
              AI-Powered Alert Generation
            </h3>
            <p className="text-sm text-purple-700">
              Enter student information below and our AI will analyze multiple parameters including attendance, 
              academic performance, behavior, and participation to generate intelligent, actionable alerts with 
              personalized recommendations.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <User className="w-5 h-5 text-blue-600" />
            Student Information
          </h2>

          <form onSubmit={handleGenerateAlerts} className="space-y-4">
            {/* Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Student Name *
              </label>
              <div className="relative">
                <User className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Enter student name"
                  className="input-field pl-10"
                  required
                />
              </div>
            </div>

            {/* Roll Number */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Roll Number / ID *
              </label>
              <div className="relative">
                <Hash className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  name="roll_number"
                  value={formData.roll_number}
                  onChange={handleInputChange}
                  placeholder="Enter roll number or student ID"
                  className="input-field pl-10"
                  required
                />
              </div>
            </div>

            {/* Attendance */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Attendance Percentage *
              </label>
              <div className="relative">
                <Calendar className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="number"
                  name="attendance_percentage"
                  value={formData.attendance_percentage}
                  onChange={handleInputChange}
                  placeholder="0-100"
                  min="0"
                  max="100"
                  step="0.1"
                  className="input-field pl-10"
                  required
                />
                <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 text-sm">
                  %
                </span>
              </div>
            </div>

            {/* Academic Performance */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Academic Performance (GPA or Marks) *
              </label>
              <div className="relative">
                <TrendingUp className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="number"
                  name="academic_performance"
                  value={formData.academic_performance}
                  onChange={handleInputChange}
                  placeholder="e.g., 3.5 (GPA) or 85 (Marks)"
                  min="0"
                  step="0.01"
                  className="input-field pl-10"
                  required
                />
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Enter GPA (0-4.0) or percentage marks (0-100)
              </p>
            </div>

            {/* Participation Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Participation / Engagement Level
              </label>
              <div className="relative">
                <Users className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <select
                  name="participation_level"
                  value={formData.participation_level}
                  onChange={handleInputChange}
                  className="input-field pl-10"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            {/* Behavior Notes */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Behavior / Discipline Notes
              </label>
              <div className="relative">
                <MessageSquare className="w-5 h-5 absolute left-3 top-3 text-gray-400" />
                <textarea
                  name="behavior_notes"
                  value={formData.behavior_notes}
                  onChange={handleInputChange}
                  placeholder="Any behavioral observations or discipline notes..."
                  rows="3"
                  className="input-field pl-10 resize-none"
                />
              </div>
            </div>

            {/* Additional Comments */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Additional Comments
              </label>
              <div className="relative">
                <FileText className="w-5 h-5 absolute left-3 top-3 text-gray-400" />
                <textarea
                  name="additional_comments"
                  value={formData.additional_comments}
                  onChange={handleInputChange}
                  placeholder="Any other relevant information..."
                  rows="3"
                  className="input-field pl-10 resize-none"
                />
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex-1 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Generate Alerts
                  </>
                )}
              </button>
              
              <button
                type="button"
                onClick={handleReset}
                disabled={loading}
                className="btn-secondary flex items-center gap-2"
              >
                <RefreshCw className="w-4 h-4" />
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* Generated Alerts Display */}
        <div className="space-y-6">
          {generatedAlerts ? (
            <>
              {/* Summary Card */}
              <div className="card bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-bold text-gray-900">
                    Analysis Summary
                  </h3>
                  {generatedAlerts.ai_powered && (
                    <span className="inline-flex items-center gap-1 px-3 py-1 bg-purple-100 text-purple-800 text-xs font-semibold rounded-full">
                      <Sparkles className="w-3 h-3" />
                      AI Powered
                    </span>
                  )}
                </div>
                
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Student:</span>
                    <span className="font-semibold text-gray-900">{generatedAlerts.student_name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Roll Number:</span>
                    <span className="font-semibold text-gray-900">{generatedAlerts.student_roll_number}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Alerts:</span>
                    <span className="font-semibold text-gray-900">{generatedAlerts.summary.total_alerts}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">High Priority:</span>
                    <span className="font-semibold text-red-600">{generatedAlerts.summary.high_priority_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Action Required:</span>
                    <span className="font-semibold text-orange-600">{generatedAlerts.summary.action_required_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Confidence:</span>
                    <span className="font-semibold text-green-600">
                      {(generatedAlerts.summary.average_confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>

                <button
                  onClick={handleSaveAlerts}
                  disabled={loading}
                  className="btn-primary w-full mt-4 flex items-center justify-center gap-2"
                >
                  <Save className="w-4 h-4" />
                  Save Alerts to Dashboard
                </button>
              </div>

              {/* Alerts List */}
              <div className="space-y-4">
                <h3 className="text-lg font-bold text-gray-900">
                  Generated Alerts ({generatedAlerts.alerts.length})
                </h3>
                
                {generatedAlerts.alerts.map((alert, index) => (
                  <div
                    key={index}
                    className={`card border-l-4 ${getAlertBorderColor(alert.alert_type)} hover:shadow-md transition-shadow`}
                  >
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 mt-1">
                        {getAlertIcon(alert.alert_type)}
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-2 flex-wrap">
                          <h4 className="text-base font-semibold text-gray-900">
                            {alert.title}
                          </h4>
                          {getPriorityBadge(alert.priority)}
                          {alert.action_required && (
                            <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800">
                              Action Required
                            </span>
                          )}
                        </div>
                        
                        <p className="text-sm text-gray-700 mb-3">
                          {alert.message}
                        </p>
                        
                        {alert.suggestions.length > 0 && (
                          <div className="mb-3">
                            <p className="text-xs font-medium text-gray-700 mb-1">
                              Suggested Actions:
                            </p>
                            <ul className="text-xs text-gray-600 space-y-1">
                              {alert.suggestions.map((suggestion, idx) => (
                                <li key={idx} className="flex items-start gap-2">
                                  <span className="w-1 h-1 bg-gray-400 rounded-full mt-1.5 flex-shrink-0"></span>
                                  <span>{suggestion}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        
                        <div className="pt-2 border-t border-gray-100">
                          <p className="text-xs text-gray-500 italic">
                            <span className="font-medium">AI Reasoning:</span> {alert.reasoning}
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            Confidence: {(alert.confidence_score * 100).toFixed(0)}% • 
                            Category: {alert.category}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="card text-center py-12">
              <AlertCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No Alerts Generated Yet
              </h3>
              <p className="text-gray-600 text-sm">
                Fill in the student information form and click "Generate Alerts" to see AI-powered analysis and recommendations.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AlertGenerator
