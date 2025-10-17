import React, { useState, useEffect } from 'react'
import { 
  Calendar, 
  CheckCircle, 
  XCircle, 
  Clock, 
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Users
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts'
import useStudentStore from '../store/studentStore'

const AttendanceTracking = () => {
  const { attendanceData, setAttendanceData } = useStudentStore()
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth())
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear())

  useEffect(() => {
    // Mock detailed attendance data
    const mockAttendanceData = {
      overall: 92,
      thisWeek: 100,
      thisMonth: 95,
      target: 95,
      totalDays: 180,
      presentDays: 166,
      absentDays: 14,
      lateArrivals: 8,
      earlyDismissals: 3,
      
      monthlyTrend: [
        { month: 'Jan', attendance: 96, target: 95 },
        { month: 'Feb', attendance: 94, target: 95 },
        { month: 'Mar', attendance: 98, target: 95 },
        { month: 'Apr', attendance: 91, target: 95 },
        { month: 'May', attendance: 93, target: 95 },
        { month: 'Jun', attendance: 97, target: 95 },
        { month: 'Jul', attendance: 89, target: 95 },
        { month: 'Aug', attendance: 95, target: 95 },
        { month: 'Sep', attendance: 92, target: 95 },
        { month: 'Oct', attendance: 94, target: 95 }
      ],

      weeklyData: [
        { day: 'Monday', present: true, time: '08:00', status: 'on-time' },
        { day: 'Tuesday', present: true, time: '08:15', status: 'late' },
        { day: 'Wednesday', present: false, time: null, status: 'absent' },
        { day: 'Thursday', present: true, time: '07:55', status: 'early' },
        { day: 'Friday', present: true, time: '08:00', status: 'on-time' }
      ],

      subjectAttendance: [
        { subject: 'Mathematics', attended: 28, total: 30, percentage: 93 },
        { subject: 'Science', attended: 27, total: 30, percentage: 90 },
        { subject: 'English', attended: 29, total: 30, percentage: 97 },
        { subject: 'History', attended: 26, total: 30, percentage: 87 },
        { subject: 'Geography', attended: 28, total: 30, percentage: 93 }
      ],

      calendarData: generateCalendarData(),

      attendanceAlerts: [
        {
          id: 1,
          type: 'warning',
          message: 'Attendance dropped below 95% this month',
          date: '2024-10-15',
          severity: 'medium'
        },
        {
          id: 2,
          type: 'info',
          message: 'Perfect attendance this week!',
          date: '2024-10-14',
          severity: 'low'
        }
      ]
    }
    
    setAttendanceData(mockAttendanceData)
  }, [])

  function generateCalendarData() {
    const data = []
    const today = new Date()
    const currentMonth = today.getMonth()
    const currentYear = today.getFullYear()
    
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate()
    
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(currentYear, currentMonth, day)
      const dayOfWeek = date.getDay()
      
      // Skip weekends
      if (dayOfWeek === 0 || dayOfWeek === 6) continue
      
      // Generate random attendance data
      const isPresent = Math.random() > 0.1 // 90% attendance rate
      const isLate = isPresent && Math.random() > 0.85 // 15% late rate
      
      data.push({
        date: day,
        present: isPresent,
        late: isLate,
        status: !isPresent ? 'absent' : isLate ? 'late' : 'present'
      })
    }
    
    return data
  }

  const getAttendanceColor = (percentage) => {
    if (percentage >= 95) return 'text-green-600'
    if (percentage >= 90) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'present':
      case 'on-time':
      case 'early':
        return <CheckCircle className="w-5 h-5 text-green-600" />
      case 'late':
        return <Clock className="w-5 h-5 text-yellow-600" />
      case 'absent':
        return <XCircle className="w-5 h-5 text-red-600" />
      default:
        return null
    }
  }

  const StatCard = ({ title, value, subtitle, icon: Icon, trend, color = "primary" }) => (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className={`text-2xl font-bold text-${color}-600`}>{value}</p>
          {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
          {trend && (
            <div className={`flex items-center mt-1 ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {trend > 0 ? (
                <TrendingUp className="w-4 h-4 mr-1" />
              ) : (
                <TrendingDown className="w-4 h-4 mr-1" />
              )}
              <span className="text-sm font-medium">{Math.abs(trend)}%</span>
            </div>
          )}
        </div>
        <div className={`p-3 bg-${color}-50 rounded-full`}>
          <Icon className={`w-6 h-6 text-${color}-600`} />
        </div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Attendance Tracking</h1>
          <p className="text-gray-600">Monitor your child's attendance patterns and trends</p>
        </div>
        
        <div className="flex space-x-4">
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
            className="input-field"
          >
            {Array.from({ length: 12 }, (_, i) => (
              <option key={i} value={i}>
                {new Date(2024, i).toLocaleString('default', { month: 'long' })}
              </option>
            ))}
          </select>
          
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(parseInt(e.target.value))}
            className="input-field"
          >
            <option value={2024}>2024</option>
            <option value={2023}>2023</option>
          </select>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Overall Attendance"
          value={`${attendanceData?.overall}%`}
          subtitle={`${attendanceData?.presentDays}/${attendanceData?.totalDays} days`}
          icon={Calendar}
          trend={attendanceData?.overall >= 95 ? 2 : -3}
          color="primary"
        />
        <StatCard
          title="This Week"
          value={`${attendanceData?.thisWeek}%`}
          subtitle="5/5 days present"
          icon={CheckCircle}
          color="green"
        />
        <StatCard
          title="Late Arrivals"
          value={attendanceData?.lateArrivals}
          subtitle="This semester"
          icon={Clock}
          color="yellow"
        />
        <StatCard
          title="Absent Days"
          value={attendanceData?.absentDays}
          subtitle="This semester"
          icon={XCircle}
          color="red"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Attendance Trend */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Attendance Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={attendanceData?.monthlyTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis domain={[80, 100]} />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="attendance" 
                stroke="#3b82f6" 
                strokeWidth={3}
                name="Attendance %"
              />
              <Line 
                type="monotone" 
                dataKey="target" 
                stroke="#ef4444" 
                strokeDasharray="5 5"
                name="Target %"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Subject-wise Attendance */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Subject-wise Attendance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={attendanceData?.subjectAttendance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="subject" />
              <YAxis domain={[80, 100]} />
              <Tooltip />
              <Bar dataKey="percentage" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* This Week's Attendance */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">This Week's Attendance</h3>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {attendanceData?.weeklyData?.map((day, index) => (
            <div key={index} className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="font-medium text-gray-900 mb-2">{day.day}</p>
              <div className="flex justify-center mb-2">
                {getStatusIcon(day.status)}
              </div>
              <p className="text-sm text-gray-600">
                {day.present ? day.time : 'Absent'}
              </p>
              <p className={`text-xs font-medium ${
                day.status === 'on-time' || day.status === 'early' ? 'text-green-600' :
                day.status === 'late' ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {day.status === 'on-time' ? 'On Time' :
                 day.status === 'early' ? 'Early' :
                 day.status === 'late' ? 'Late' : 'Absent'}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Calendar View & Subject Attendance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Calendar */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Attendance Calendar - {new Date(selectedYear, selectedMonth).toLocaleString('default', { month: 'long', year: 'numeric' })}
          </h3>
          <div className="grid grid-cols-7 gap-2 mb-4">
            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(day => (
              <div key={day} className="text-center text-sm font-medium text-gray-500 py-2">
                {day}
              </div>
            ))}
          </div>
          <div className="grid grid-cols-7 gap-2">
            {attendanceData?.calendarData?.map((day, index) => (
              <div
                key={index}
                className={`aspect-square flex items-center justify-center text-sm rounded-lg ${
                  day.status === 'present' ? 'bg-green-100 text-green-800' :
                  day.status === 'late' ? 'bg-yellow-100 text-yellow-800' :
                  day.status === 'absent' ? 'bg-red-100 text-red-800' : 'bg-gray-100'
                }`}
              >
                {day.date}
              </div>
            ))}
          </div>
          <div className="flex items-center justify-center space-x-6 mt-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-100 rounded"></div>
              <span>Present</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-yellow-100 rounded"></div>
              <span>Late</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-100 rounded"></div>
              <span>Absent</span>
            </div>
          </div>
        </div>

        {/* Subject Attendance Details */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Subject Attendance Details</h3>
          <div className="space-y-4">
            {attendanceData?.subjectAttendance?.map((subject, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-50 rounded-lg">
                    <Users className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{subject.subject}</p>
                    <p className="text-sm text-gray-600">
                      {subject.attended}/{subject.total} classes
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`text-lg font-bold ${getAttendanceColor(subject.percentage)}`}>
                    {subject.percentage}%
                  </p>
                  <div className="w-24 bg-gray-200 rounded-full h-2 mt-1">
                    <div
                      className={`h-2 rounded-full ${
                        subject.percentage >= 95 ? 'bg-green-500' :
                        subject.percentage >= 90 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${subject.percentage}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Attendance Alerts */}
      {attendanceData?.attendanceAlerts?.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Attendance Alerts</h3>
          <div className="space-y-3">
            {attendanceData.attendanceAlerts.map((alert) => (
              <div key={alert.id} className="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
                <div className={`p-1 rounded-full ${
                  alert.type === 'warning' ? 'bg-yellow-100' : 'bg-blue-100'
                }`}>
                  <AlertTriangle className={`w-5 h-5 ${
                    alert.type === 'warning' ? 'text-yellow-600' : 'text-blue-600'
                  }`} />
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{alert.message}</p>
                  <p className="text-sm text-gray-500">{alert.date}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default AttendanceTracking
