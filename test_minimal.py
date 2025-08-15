#!/usr/bin/env python3
"""
Minimal test to verify basic FastAPI functionality
"""

import os
import uvicorn
from fastapi import FastAPI

# Create minimal app
app = FastAPI(title="Downtify Test")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting minimal test app on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
