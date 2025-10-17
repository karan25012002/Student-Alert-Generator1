import React, { useState, useEffect } from 'react'
import { 
  Activity, 
  Clock, 
  MessageSquare, 
  BookOpen, 
  Monitor,
  TrendingUp,
  TrendingDown,
  Target,
  Zap,
  Users,
  Award
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
  Bar,
  RadialBarChart,
  RadialBar,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import useStudentStore from '../store/studentStore'

const EngagementInsights = () => {
  const { engagementData, setEngagementData } = useStudentStore()
  const [selectedPeriod, setSelectedPeriod] = useState('week')
  const [selectedMetric, setSelectedMetric] = useState('all')

  useEffect(() => {
    // Mock detailed engagement data
    const mockEngagementData = {
      overallScore: 85,
      studyTime: 4.5,
      participation: 88,
      onlineActivity: 82,
      focusTime: 3.2,
      
      weeklyEngagement: [
        { day: 'Mon', hours: 3.5, participation: 85, focus: 80 },
        { day: 'Tue', hours: 4.2, participation: 90, focus: 85 },
        { day: 'Wed', hours: 2.8, participation: 75, focus: 70 },
        { day: 'Thu', hours: 5.1, participation: 95, focus: 90 },
        { day: 'Fri', hours: 4.0, participation: 88, focus: 82 },
        { day: 'Sat', hours: 6.2, participation: 92, focus: 88 },
        { day: 'Sun', hours: 3.8, participation: 78, focus: 75 }
      ],

      monthlyTrend: [
        { month: 'Jan', engagement: 78, studyTime: 3.8, participation: 82 },
        { month: 'Feb', engagement: 82, studyTime: 4.1, participation: 85 },
        { month: 'Mar', engagement: 85, studyTime: 4.3, participation: 87 },
        { month: 'Apr', engagement: 80, studyTime: 3.9, participation: 83 },
        { month: 'May', engagement: 88, studyTime: 4.6, participation: 90 },
        { month: 'Jun', engagement: 86, studyTime: 4.4, participation: 88 },
        { month: 'Jul', engagement: 84, studyTime: 4.2, participation: 86 },
        { month: 'Aug', engagement: 87, studyTime: 4.5, participation: 89 },
        { month: 'Sep', engagement: 89, studyTime: 4.7, participation: 91 },
        { month: 'Oct', engagement: 85, studyTime: 4.5, participation: 88 }
      ],

      subjectEngagement: [
        { subject: 'Mathematics', engagement: 92, timeSpent: 8.5, participation: 95 },
        { subject: 'Science', engagement: 88, timeSpent: 7.2, participation: 90 },
        { subject: 'English', engagement: 85, timeSpent: 6.8, participation: 87 },
        { subject: 'History', engagement: 75, timeSpent: 5.2, participation: 78 },
        { subject: 'Geography', engagement: 82, timeSpent: 6.0, participation: 85 }
      ],

      activityBreakdown: [
        { activity: 'Reading', hours: 12.5, percentage: 35 },
        { activity: 'Problem Solving', hours: 10.2, percentage: 28 },
        { activity: 'Research', hours: 7.8, percentage: 22 },
        { activity: 'Discussion', hours: 5.5, percentage: 15 }
      ],

      onlineMetrics: {
        totalSessions: 45,
        averageSessionTime: 52, // minutes
        completionRate: 94,
        interactionScore: 87,
        resourcesAccessed: 128,
        forumsParticipation: 23
      },

      engagementGoals: [
        { metric: 'Study Time', current: 4.5, target: 5.0, percentage: 90 },
        { metric: 'Participation', current: 88, target: 90, percentage: 98 },
        { metric: 'Focus Time', current: 3.2, target: 4.0, percentage: 80 },
        { metric: 'Online Activity', current: 82, target: 85, percentage: 96 }
      ],

      weeklyInsights: [
        {
          type: 'positive',
          title: 'Great Focus Improvement',
          description: 'Focus time increased by 15% this week compared to last week.',
          icon: 'focus'
        },
        {
          type: 'neutral',
          title: 'Consistent Study Pattern',
          description: 'Maintaining steady 4+ hours of daily study time.',
          icon: 'time'
        },
        {
          type: 'improvement',
          title: 'Math Engagement Peak',
          description: 'Highest engagement scores recorded in Mathematics this month.',
          icon: 'subject'
        }
      ]
    }
    
    setEngagementData(mockEngagementData)
  }, [])

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

  const MetricCard = ({ title, value, subtitle, icon: Icon, trend, color = "primary", target }) => (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`p-2 bg-${color}-50 rounded-lg`}>
            <Icon className={`w-6 h-6 text-${color}-600`} />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className={`text-2xl font-bold text-${color}-600`}>{value}</p>
            {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
          </div>
        </div>
        {trend && (
          <div className={`flex items-center ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
            {trend > 0 ? (
              <TrendingUp className="w-5 h-5 mr-1" />
            ) : (
              <TrendingDown className="w-5 h-5 mr-1" />
            )}
            <span className="text-sm font-medium">{Math.abs(trend)}%</span>
          </div>
        )}
      </div>
      {target && (
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>Progress to Goal</span>
            <span>{target.percentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full bg-${color}-500`}
              style={{ width: `${target.percentage}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  )

  const InsightCard = ({ insight }) => {
    const getInsightIcon = (iconType) => {
      switch (iconType) {
        case 'focus': return <Target className="w-5 h-5" />
        case 'time': return <Clock className="w-5 h-5" />
        case 'subject': return <BookOpen className="w-5 h-5" />
        default: return <Activity className="w-5 h-5" />
      }
    }

    const getInsightColor = (type) => {
      switch (type) {
        case 'positive': return 'green'
        case 'improvement': return 'blue'
        case 'neutral': return 'gray'
        default: return 'blue'
      }
    }

    const color = getInsightColor(insight.type)

    return (
      <div className="card">
        <div className="flex items-start space-x-3">
          <div className={`p-2 bg-${color}-50 rounded-lg`}>
            <div className={`text-${color}-600`}>
              {getInsightIcon(insight.icon)}
            </div>
          </div>
          <div className="flex-1">
            <h4 className="font-medium text-gray-900">{insight.title}</h4>
            <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Engagement Insights</h1>
          <p className="text-gray-600">Track your child's learning engagement and study patterns</p>
        </div>
        
        <div className="flex space-x-4">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="input-field"
          >
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="semester">This Semester</option>
          </select>
          
          <select
            value={selectedMetric}
            onChange={(e) => setSelectedMetric(e.target.value)}
            className="input-field"
          >
            <option value="all">All Metrics</option>
            <option value="time">Study Time</option>
            <option value="participation">Participation</option>
            <option value="focus">Focus Time</option>
          </select>
        </div>
      </div>

      {/* Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Overall Engagement"
          value={`${engagementData?.overallScore}%`}
          subtitle="This week"
          icon={Activity}
          trend={5}
          color="primary"
          target={{ percentage: 85 }}
        />
        <MetricCard
          title="Daily Study Time"
          value={`${engagementData?.studyTime}h`}
          subtitle="Average per day"
          icon={Clock}
          trend={8}
          color="green"
          target={{ percentage: 90 }}
        />
        <MetricCard
          title="Participation Rate"
          value={`${engagementData?.participation}%`}
          subtitle="Class participation"
          icon={MessageSquare}
          trend={-2}
          color="blue"
          target={{ percentage: 98 }}
        />
        <MetricCard
          title="Focus Time"
          value={`${engagementData?.focusTime}h`}
          subtitle="Deep focus sessions"
          icon={Target}
          trend={15}
          color="purple"
          target={{ percentage: 80 }}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Engagement Trend */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Engagement Pattern</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={engagementData?.weeklyEngagement}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="hours" 
                stroke="#3b82f6" 
                strokeWidth={3}
                name="Study Hours"
              />
              <Line 
                type="monotone" 
                dataKey="participation" 
                stroke="#10b981" 
                strokeWidth={2}
                name="Participation %"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Subject Engagement */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Subject-wise Engagement</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={engagementData?.subjectEngagement}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="subject" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="engagement" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Activity Breakdown & Goals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Breakdown */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Study Activity Breakdown</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={engagementData?.activityBreakdown}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ activity, percentage }) => `${activity}: ${percentage}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="hours"
              >
                {engagementData?.activityBreakdown?.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Engagement Goals */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Engagement Goals</h3>
          <div className="space-y-4">
            {engagementData?.engagementGoals?.map((goal, index) => (
              <div key={index} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-900">{goal.metric}</span>
                  <span className="text-sm text-gray-600">
                    {goal.current} / {goal.target}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full ${
                      goal.percentage >= 95 ? 'bg-green-500' :
                      goal.percentage >= 80 ? 'bg-blue-500' :
                      goal.percentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${goal.percentage}%` }}
                  ></div>
                </div>
                <div className="text-right text-sm text-gray-500">
                  {goal.percentage}% of target
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Online Learning Metrics */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Online Learning Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <Monitor className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{engagementData?.onlineMetrics?.totalSessions}</p>
            <p className="text-sm text-gray-600">Total Sessions</p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <Clock className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{engagementData?.onlineMetrics?.averageSessionTime}m</p>
            <p className="text-sm text-gray-600">Avg Session Time</p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <Award className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{engagementData?.onlineMetrics?.completionRate}%</p>
            <p className="text-sm text-gray-600">Completion Rate</p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <Zap className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{engagementData?.onlineMetrics?.interactionScore}%</p>
            <p className="text-sm text-gray-600">Interaction Score</p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <BookOpen className="w-8 h-8 text-indigo-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{engagementData?.onlineMetrics?.resourcesAccessed}</p>
            <p className="text-sm text-gray-600">Resources Accessed</p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <Users className="w-8 h-8 text-pink-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{engagementData?.onlineMetrics?.forumsParticipation}</p>
            <p className="text-sm text-gray-600">Forum Posts</p>
          </div>
        </div>
      </div>

      {/* Monthly Trend */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Engagement Trend</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={engagementData?.monthlyTrend}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Line 
              type="monotone" 
              dataKey="engagement" 
              stroke="#3b82f6" 
              strokeWidth={3}
              name="Engagement Score"
            />
            <Line 
              type="monotone" 
              dataKey="studyTime" 
              stroke="#10b981" 
              strokeWidth={2}
              name="Study Time (hrs)"
            />
            <Line 
              type="monotone" 
              dataKey="participation" 
              stroke="#f59e0b" 
              strokeWidth={2}
              name="Participation %"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Weekly Insights */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Weekly Insights</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {engagementData?.weeklyInsights?.map((insight, index) => (
            <InsightCard key={index} insight={insight} />
          ))}
        </div>
      </div>

      {/* Subject Details Table */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Subject Engagement Details</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Subject
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Engagement Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Time Spent (hrs)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Participation %
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {engagementData?.subjectEngagement?.map((subject, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {subject.subject}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div className="flex items-center">
                      <span className="mr-2">{subject.engagement}%</span>
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            subject.engagement >= 90 ? 'bg-green-500' :
                            subject.engagement >= 80 ? 'bg-blue-500' :
                            subject.engagement >= 70 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${subject.engagement}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {subject.timeSpent}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {subject.participation}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      subject.engagement >= 85 ? 'bg-green-100 text-green-800' :
                      subject.engagement >= 75 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {subject.engagement >= 85 ? 'Excellent' :
                       subject.engagement >= 75 ? 'Good' : 'Needs Attention'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default EngagementInsights
