# Agentic AI - Student Progress Tracker

A comprehensive Student Progress & Engagement Tracking System for Parents with AI-powered insights and alert generation.

## 🚀 Features

### Core Features
- **Student Progress Tracking**: Monitor academic performance, attendance, and engagement
- **AI-Powered Alerts**: Intelligent alert generation based on student data analysis
- **Parent Dashboard**: Real-time insights and recommendations for parents
- **Attendance Tracking**: Monitor and analyze attendance patterns
- **Academic Performance Analysis**: Track grades and academic progress
- **Behavioral Insights**: Monitor student behavior and participation

### Technical Features
- **Real-time Updates**: Live data synchronization
- **AI-Powered Analysis**: Advanced insights using machine learning
- **Responsive Design**: Works seamlessly on all devices
- **Secure Authentication**: JWT-based user authentication
- **RESTful API**: Well-structured backend API
- **Modern Frontend**: React-based user interface

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **AI Integration**: Google Gemini API for insights
- **Authentication**: JWT tokens with secure password hashing
- **CORS Support**: Cross-origin resource sharing enabled

### Frontend (React)
- **Framework**: React with Vite
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

## 📁 Project Structure

```
Agentic_AI/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── controllers/     # Business logic controllers
│   │   ├── core/           # Configuration and security
│   │   ├── database/       # Database connection and models
│   │   ├── models/         # Data models and schemas
│   │   ├── routes/         # API route definitions
│   │   ├── services/       # AI agents and business logic
│   │   └── utils/          # Utility functions
│   ├── main.py             # Main application entry point
│   ├── requirements.txt     # Python dependencies
│   └── .env               # Environment variables
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── store/         # State management stores
│   │   ├── utils/         # Utility functions
│   │   └── api/           # API configuration
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
│
├── .gitignore             # Git ignore patterns
└── README.md              # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On Unix/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Update database URL and API keys in `.env`

5. **Start the server:**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=student_tracker

# JWT Settings
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Gemini API (for AI insights)
GOOGLE_API_KEY=your-gemini-api-key

# Environment
ENVIRONMENT=development
DEBUG=True

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:
- Register/Login endpoints available at `/api/auth/`
- Include `Authorization: Bearer <token>` header in requests

## 🤖 AI Features

### Alert Generation
- Analyzes student data (attendance, performance, behavior)
- Generates intelligent alerts with confidence scores
- Provides actionable recommendations

### Insight Generation
- Uses Google Gemini AI for advanced analysis
- Provides personalized insights and recommendations
- Supports natural language queries

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚢 Deployment

### GitHub Repository Setup

1. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub Repository:**
   - Go to [GitHub.com](https://github.com) and create a new repository.
   - Copy the repository URL (e.g., `https://github.com/username/repo-name.git`).

3. **Push to GitHub:**
   ```bash
   git remote add origin <your-repo-url>
   git branch -M main
   git push -u origin main
   ```

### Render Deployment

1. **Create Services Using YAML:**
   - Place the `render.yaml` file in your project root.
   - In Render dashboard, go to "Blueprint" and select "Deploy from YAML".
   - Connect your GitHub repository.
   - Render will create two services: backend (web) and frontend (static).

2. **Set Secrets in Render:**
   - For the backend service, add secrets:
     - `mongodb-atlas-url`: Your MongoDB Atlas connection string.
     - `secret-key`: A strong JWT secret key.
     - `google-api-key`: Your Google Gemini API key.

3. **Deploy:**
   - Render will build and deploy both services.
   - Backend: `https://student-tracker-backend.onrender.com`
   - Frontend: `https://student-tracker-frontend.onrender.com`

4. **Seamless Connection:**
   - The `render.yaml` sets `VITE_API_BASE_URL` for the frontend to point to the backend.
   - Backend CORS is configured to accept requests from the frontend URL.
   - No additional configuration needed – the apps are connected automatically.

## 📝 Development

### Code Style
- **Backend**: Follow PEP 8 guidelines
- **Frontend**: ESLint and Prettier configured

### Git Hooks
- Pre-commit hooks for code quality
- Automated testing on push

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with FastAPI, React, and modern web technologies
- AI-powered insights using Google Gemini
- Open source community contributions

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team

---

**Made with ❤️ for education and student success**
