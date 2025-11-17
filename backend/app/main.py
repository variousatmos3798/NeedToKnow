from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import topics, videos

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YouTube Tutorial Generator & Refiner",
    description="Convert YouTube videos into actionable step-by-step tutorials",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(topics.router)
app.include_router(videos.router)

@app.get("/")
def root():
    return {
        "message": "YouTube Tutorial Generator & Refiner API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
