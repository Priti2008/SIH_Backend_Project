from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime

app = FastAPI(title="SIH Border Surveillance Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

alerts_db = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

class AlertModel(BaseModel):
    camera_id: str
    alert_type: str
    severity: str
    snapshot_url: Optional[str] = "http://localhost:8000/static/sample.jpg"

@app.post("/api/v1/auth/login")
def login(credentials: dict):
    username = credentials.get("username")
    password = credentials.get("password")
    
    if username == "admin" and password == "border123":
        return {"status": "success", "token": "mock-jwt-token-xyz", "role": "admin"}
    return {"status": "error", "message": "Invalid Credentials"}, 401

@app.post("/api/v1/alerts")
async def receive_alert(alert: AlertModel):
    alert_data = alert.dict()
    alert_data["id"] = len(alerts_db) + 1
    alert_data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerts_db.append(alert_data)
    await manager.broadcast(alert_data)
    return {"status": "success", "alert": alert_data}

@app.get("/api/v1/alerts")
def get_alerts():
    return {"alerts": alerts_db}

@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)