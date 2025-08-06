@"
from fastapi import FastAPI

app = FastAPI(title="MORVO Phase 6")

@app.get("/")
def root():
    return {"message": "MORVO Phase 6 Working", "status": "success"}

@app.get("/dashboard")  
def dashboard():
    return {"message": "Dashboard endpoint working"}
"@ > main.py