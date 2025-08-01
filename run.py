#!/usr/bin/env python3
"""
FastAPI Prototype Startup Script

This script provides an easy way to run the FastAPI application
with proper configuration and development settings.
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    """Main function to run the FastAPI application"""
    
    # Load environment variables
    load_dotenv()
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "True").lower() == "true"
    
    print(f"🚀 Starting FastAPI Prototype...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"📖 ReDoc: http://{host}:{port}/redoc")
    print(f"🏥 Health Check: http://{host}:{port}/health")
    print("-" * 50)
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main() 