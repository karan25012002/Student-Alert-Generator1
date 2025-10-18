from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import os
import uvicorn
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection, seed_dummy_data, get_database
from app.routes import auth, student, alerts, insights, alert_generator

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    await seed_dummy_data()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Student Progress Tracker API",
    description="Real-time Student Progress & Engagement Tracking System for Parents",
    version="1.0.0",
    lifespan=lifespan
)

# Custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error. Please check your input data."}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)}
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
    )

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(student.router, prefix="/api/student", tags=["Student Data"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(insights.router, prefix="/api/insights", tags=["AI Insights"])
app.include_router(alert_generator.router, prefix="/api/alert-generator", tags=["Alert Generator"])

@app.get("/")
async def root():
    return {
        "message": "Student Progress Tracker API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/test-cors")
async def test_cors():
    """Test endpoint to verify CORS configuration."""
    return {
        "message": "CORS test successful",
        "allowed_origins": settings.ALLOWED_ORIGINS,
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    try:
        # Check database connection
        db = await get_database()
        # Test a simple database operation
        user_count = await db.users.count_documents({})
        student_count = await db.students.count_documents({})
        
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "database": {
                "connected": True,
                "users_count": user_count,
                "students_count": student_count
            },
            "api_routes": {
                "auth": "/api/auth/*",
                "student": "/api/student/*",
                "alerts": "/api/alerts/*",
                "insights": "/api/insights/*",
                "alert_generator": "/api/alert-generator/*"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
