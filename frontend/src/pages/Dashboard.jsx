import React, { useEffect, useState } from 'react'
import { 
  TrendingUp, 
  TrendingDown, 
  Calendar, 
  Clock, 
  Award, 
  AlertTriangle,
  BookOpen,
  Users
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import useStudentStore from '../store/studentStore'
import useAuthStore from '../store/authStore'
import { studentApi } from '../api/studentApi'
import toast from 'react-hot-toast'

const Dashboard = () => {
  const { user } = useAuthStore()
  const { 
    studentData, 
    academicData, 
    attendanceData, 
    engagementData, 
    alerts,
    setStudentData,
    setAcademicData,
    setAttendanceData,
    setEngagementData,
    setAlerts
  } = useStudentStore()

  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      
      // Mock data for demonstration
      const mockStudentData = {
        id: 'STU001',
        name: user?.studentName || 'John Doe',
        grade: '10th Grade',
        class: 'Section A',
        overallGPA: 3.8,
        attendance: 92,
        engagementScore: 85
      }

      const mockAcademicData = {
        subjects: [
          { name: 'Mathematics', grade: 'A-', score: 88, trend: 'up' },
          { name: 'Science', grade: 'B+', score: 85, trend: 'up' },
          { name: 'English', grade: 'A', score: 92, trend: 'stable' },
          { name: 'History', grade: 'B', score: 78, trend: 'down' },
          { name: 'Geography', grade: 'A-', score: 87, trend: 'up' }
        ],
        recentGrades: [
          { date: '2024-10-15', subject: 'Math', assignment: 'Quiz 3', score: 95 },
          { date: '2024-10-14', subject: 'Science', assignment: 'Lab Report', score: 88 },
          { date: '2024-10-13', subject: 'English', assignment: 'Essay', score: 92 }
        ],
        monthlyProgress: [
          { month: 'Aug', gpa: 3.6 },
          { month: 'Sep', gpa: 3.7 },
          { month: 'Oct', gpa: 3.8 }
        ]
      }

      const mockAttendanceData = {
        overall: 92,
        thisWeek: 100,
        thisMonth: 95,
        weeklyData: [
          { day: 'Mon', present: true },
          { day: 'Tue', present: true },
          { day: 'Wed', present: false },
          { day: 'Thu', present: true },
          { day: 'Fri', present: true }
        ],
        monthlyTrend: [
          { month: 'Aug', attendance: 90 },
          { month: 'Sep', attendance: 94 },
          { month: 'Oct', attendance: 92 }
        ]
      }

      const mockEngagementData = {
        overallScore: 85,
        studyTime: 4.5,
        participation: 88,
        onlineActivity: 82,
        weeklyEngagement: [
          { day: 'Mon', hours: 3.5 },
          { day: 'Tue', hours: 4.2 },
          { day: 'Wed', hours: 2.8 },
          { day: 'Thu', hours: 5.1 },
          { day: 'Fri', hours: 4.0 },
          { day: 'Sat', hours: 6.2 },
          { day: 'Sun', hours: 3.8 }
        ]
      }

      const mockAlerts = [
        {
          id: 1,
          type: 'warning',
          title: 'Math Performance Decline',
          message: 'Math scores have dropped by 8% this week. Consider additional practice.',
          date: '2024-10-16',
          read: false,
          priority: 'medium'
        },
        {
          id: 2,
          type: 'info',
          title: 'Excellent English Performance',
          message: 'Your child scored 95% on the recent English essay. Great work!',
          date: '2024-10-15',
          read: false,
          priority: 'low'
        }
      ]

      setStudentData(mockStudentData)
      setAcademicData(mockAcademicData)
      setAttendanceData(mockAttendanceData)
      setEngagementData(mockEngagementData)
      setAlerts(mockAlerts)

    } catch (error) {
      console.error('Dashboard error:', error)
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Failed to load dashboard data'
      toast.error(typeof errorMessage === 'string' ? errorMessage : 'Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  const StatCard = ({ title, value, change, icon: Icon, trend }) => (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change && (
            <div className={`flex items-center mt-1 ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
              {trend === 'up' ? (
                <TrendingUp className="w-4 h-4 mr-1" />
              ) : (
                <TrendingDown className="w-4 h-4 mr-1" />
              )}
              <span className="text-sm font-medium">{change}</span>
            </div>
          )}
        </div>
        <div className="p-3 bg-blue-50 rounded-full">
          <Icon className="w-6 h-6 text-blue-600" />
        </div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here's your child's progress overview.</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Student: {studentData?.name}</p>
          <p className="text-sm text-gray-500">{studentData?.grade} - {studentData?.class}</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Overall GPA"
          value={studentData?.overallGPA}
          change="+0.2"
          trend="up"
          icon={Award}
        />
        <StatCard
          title="Attendance Rate"
          value={`${studentData?.attendance}%`}
          change="-2%"
          trend="down"
          icon={Calendar}
        />
        <StatCard
          title="Engagement Score"
          value={`${studentData?.engagementScore}%`}
          change="+5%"
          trend="up"
          icon={TrendingUp}
        />
        <StatCard
          title="Study Hours/Week"
          value={`${engagementData?.studyTime}h`}
          change="+0.5h"
          trend="up"
          icon={Clock}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Academic Progress Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Academic Progress</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={academicData?.monthlyProgress}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis domain={[3.0, 4.0]} />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="gpa" 
                stroke="#3b82f6" 
                strokeWidth={3}
                dot={{ fill: '#3b82f6', strokeWidth: 2, r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Weekly Engagement Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Study Hours</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={engagementData?.weeklyEngagement}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="hours" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity & Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Grades */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Grades</h3>
          <div className="space-y-3">
            {academicData?.recentGrades?.map((grade, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{String(grade.subject || 'Unknown')}</p>
                  <p className="text-sm text-gray-600">{String(grade.assignment || 'N/A')}</p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">{String(grade.grade || 'N/A')}</p>
                  <p className="text-sm text-gray-600">{String(grade.date || 'N/A')}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Alerts</h3>
          <div className="space-y-3">
            {alerts?.slice(0, 3).map((alert) => (
              <div key={alert.id || Math.random()} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className={`p-1 rounded-full ${
                  alert.type === 'warning' ? 'bg-yellow-100' : 'bg-blue-100'
                }`}>
                  <AlertTriangle className={`w-4 h-4 ${
                    alert.type === 'warning' ? 'text-yellow-600' : 'text-blue-600'
                  }`} />
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{String(alert.title || 'Alert')}</p>
                  <p className="text-sm text-gray-600">{String(alert.message || 'No message')}</p>
                  <p className="text-xs text-gray-500 mt-1">{String(alert.date || 'No date')}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Subject Performance Overview */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Subject Performance</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {academicData?.subjects?.map((subject, index) => (
            <div key={index} className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-center mb-2">
                <BookOpen className="w-8 h-8 text-blue-600" />
              </div>
              <h4 className="font-medium text-gray-900">{String(subject.name || 'Subject')}</h4>
              <p className="text-2xl font-bold text-blue-600 mt-1">{String(subject.grade || 'N/A')}</p>
              <p className="text-sm text-gray-600">{String(subject.score || 0)}%</p>
              <div className={`flex items-center justify-center mt-2 ${
                subject.trend === 'up' ? 'text-green-600' : 
                subject.trend === 'down' ? 'text-red-600' : 'text-gray-600'
              }`}>
                {subject.trend === 'up' && <TrendingUp className="w-4 h-4" />}
                {subject.trend === 'down' && <TrendingDown className="w-4 h-4" />}
                {subject.trend === 'stable' && <div className="w-4 h-0.5 bg-gray-400"></div>}
              </div>
            </div>
          )) || []}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
