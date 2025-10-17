import React, { useState, useEffect } from 'react'
import { 
  BookOpen, 
  TrendingUp, 
  TrendingDown, 
  Award, 
  Target,
  Calendar,
  Filter
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
  PieChart,
  Pie,
  Cell
} from 'recharts'
import useStudentStore from '../store/studentStore'

const AcademicPerformance = () => {
  const { academicData, setAcademicData } = useStudentStore()
  const [selectedPeriod, setSelectedPeriod] = useState('semester')
  const [selectedSubject, setSelectedSubject] = useState('all')

  useEffect(() => {
    // Mock detailed academic data
    const mockDetailedData = {
      subjects: [
        { 
          name: 'Mathematics', 
          grade: 'A-', 
          score: 88, 
          trend: 'up',
          assignments: [
            { name: 'Quiz 1', score: 85, date: '2024-09-15', type: 'quiz' },
            { name: 'Midterm Exam', score: 92, date: '2024-10-01', type: 'exam' },
            { name: 'Homework 5', score: 88, date: '2024-10-10', type: 'homework' }
          ],
          weeklyProgress: [
            { week: 'Week 1', score: 85 },
            { week: 'Week 2', score: 87 },
            { week: 'Week 3', score: 89 },
            { week: 'Week 4', score: 88 }
          ]
        },
        { 
          name: 'Science', 
          grade: 'B+', 
          score: 85, 
          trend: 'up',
          assignments: [
            { name: 'Lab Report 1', score: 88, date: '2024-09-20', type: 'lab' },
            { name: 'Quiz 2', score: 82, date: '2024-10-05', type: 'quiz' },
            { name: 'Project', score: 90, date: '2024-10-12', type: 'project' }
          ],
          weeklyProgress: [
            { week: 'Week 1', score: 82 },
            { week: 'Week 2', score: 84 },
            { week: 'Week 3', score: 86 },
            { week: 'Week 4', score: 85 }
          ]
        },
        { 
          name: 'English', 
          grade: 'A', 
          score: 92, 
          trend: 'stable',
          assignments: [
            { name: 'Essay 1', score: 95, date: '2024-09-18', type: 'essay' },
            { name: 'Reading Quiz', score: 89, date: '2024-10-03', type: 'quiz' },
            { name: 'Presentation', score: 94, date: '2024-10-08', type: 'presentation' }
          ],
          weeklyProgress: [
            { week: 'Week 1', score: 91 },
            { week: 'Week 2', score: 92 },
            { week: 'Week 3', score: 93 },
            { week: 'Week 4', score: 92 }
          ]
        },
        { 
          name: 'History', 
          grade: 'B', 
          score: 78, 
          trend: 'down',
          assignments: [
            { name: 'Test 1', score: 75, date: '2024-09-25', type: 'test' },
            { name: 'Research Paper', score: 82, date: '2024-10-07', type: 'paper' },
            { name: 'Quiz 3', score: 76, date: '2024-10-14', type: 'quiz' }
          ],
          weeklyProgress: [
            { week: 'Week 1', score: 82 },
            { week: 'Week 2', score: 80 },
            { week: 'Week 3', score: 79 },
            { week: 'Week 4', score: 78 }
          ]
        },
        { 
          name: 'Geography', 
          grade: 'A-', 
          score: 87, 
          trend: 'up',
          assignments: [
            { name: 'Map Project', score: 90, date: '2024-09-22', type: 'project' },
            { name: 'Quiz 1', score: 85, date: '2024-10-02', type: 'quiz' },
            { name: 'Field Report', score: 88, date: '2024-10-11', type: 'report' }
          ],
          weeklyProgress: [
            { week: 'Week 1', score: 85 },
            { week: 'Week 2', score: 86 },
            { week: 'Week 3', score: 87 },
            { week: 'Week 4', score: 87 }
          ]
        }
      ],
      overallProgress: [
        { month: 'August', gpa: 3.6, attendance: 95 },
        { month: 'September', gpa: 3.7, attendance: 92 },
        { month: 'October', gpa: 3.8, attendance: 94 }
      ],
      gradeDistribution: [
        { grade: 'A', count: 12, percentage: 40 },
        { grade: 'B', count: 10, percentage: 33 },
        { grade: 'C', count: 6, percentage: 20 },
        { grade: 'D', count: 2, percentage: 7 }
      ]
    }
    
    setAcademicData(mockDetailedData)
  }, [])

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

  const getSubjectData = () => {
    if (!academicData?.subjects) return []
    return selectedSubject === 'all' 
      ? academicData.subjects 
      : academicData.subjects.filter(s => s.name === selectedSubject)
  }

  const SubjectCard = ({ subject }) => (
    <div className="card hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-50 rounded-lg">
            <BookOpen className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">{subject.name}</h3>
            <p className="text-sm text-gray-600">Current Grade: {subject.grade}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-blue-600">{subject.score}%</p>
          <div className={`flex items-center ${
            subject.trend === 'up' ? 'text-green-600' : 
            subject.trend === 'down' ? 'text-red-600' : 'text-gray-600'
          }`}>
            {subject.trend === 'up' && <TrendingUp className="w-4 h-4 mr-1" />}
            {subject.trend === 'down' && <TrendingDown className="w-4 h-4 mr-1" />}
            <span className="text-sm">{subject.trend}</span>
          </div>
        </div>
      </div>
      
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Weekly Progress</h4>
        <ResponsiveContainer width="100%" height={120}>
          <LineChart data={subject.weeklyProgress}>
            <Line 
              type="monotone" 
              dataKey="score" 
              stroke="#3b82f6" 
              strokeWidth={2}
              dot={{ fill: '#3b82f6', r: 3 }}
            />
            <XAxis dataKey="week" hide />
            <YAxis hide />
            <Tooltip />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-2">Recent Assignments</h4>
        <div className="space-y-2">
          {subject.assignments?.slice(0, 3).map((assignment, index) => (
            <div key={index} className="flex items-center justify-between text-sm">
              <span className="text-gray-600">{assignment.name}</span>
              <span className={`font-medium ${
                assignment.score >= 90 ? 'text-green-600' : 
                assignment.score >= 80 ? 'text-blue-600' : 'text-yellow-600'
              }`}>
                {assignment.score}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Academic Performance</h1>
          <p className="text-gray-600">Detailed view of your child's academic progress</p>
        </div>
        
        <div className="flex space-x-4">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="input-field"
          >
            <option value="semester">This Semester</option>
            <option value="quarter">This Quarter</option>
            <option value="month">This Month</option>
          </select>
          
          <select
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
            className="input-field"
          >
            <option value="all">All Subjects</option>
            {academicData?.subjects?.map((subject) => (
              <option key={subject.name} value={subject.name}>
                {subject.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card text-center">
          <Award className="w-8 h-8 text-blue-600 mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900">3.8</p>
          <p className="text-sm text-gray-600">Current GPA</p>
        </div>
        <div className="card text-center">
          <Target className="w-8 h-8 text-green-600 mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900">86%</p>
          <p className="text-sm text-gray-600">Average Score</p>
        </div>
        <div className="card text-center">
          <TrendingUp className="w-8 h-8 text-blue-600 mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900">+5%</p>
          <p className="text-sm text-gray-600">Improvement</p>
        </div>
        <div className="card text-center">
          <BookOpen className="w-8 h-8 text-purple-600 mx-auto mb-2" />
          <p className="text-2xl font-bold text-gray-900">5</p>
          <p className="text-sm text-gray-600">Subjects</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Overall Progress Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Overall Progress Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={academicData?.overallProgress}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="gpa" 
                stroke="#3b82f6" 
                strokeWidth={3}
                name="GPA"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Grade Distribution */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Grade Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={academicData?.gradeDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ grade, percentage }) => `${grade}: ${percentage}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="count"
              >
                {academicData?.gradeDistribution?.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Subject Performance Cards */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Subject Performance</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {getSubjectData().map((subject, index) => (
            <SubjectCard key={index} subject={subject} />
          ))}
        </div>
      </div>

      {/* Recent Assignments Table */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Assignments</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Subject
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Assignment
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Score
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {academicData?.subjects?.flatMap(subject => 
                subject.assignments?.map(assignment => ({
                  ...assignment,
                  subject: subject.name
                }))
              ).slice(0, 10).map((assignment, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {assignment.subject}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {assignment.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                      {assignment.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {assignment.date}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <span className={`${
                      assignment.score >= 90 ? 'text-green-600' : 
                      assignment.score >= 80 ? 'text-blue-600' : 
                      assignment.score >= 70 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {assignment.score}%
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

export default AcademicPerformance
