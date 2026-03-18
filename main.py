from fastapi import FastAPI
from pydantic import BaseModel
import agent_service
import todo_service
from fastapi.middleware.cors import CORSMiddleware

# 1. יצירת השרת עם כותרת ותיאור שיופיעו ב-Swagger
app = FastAPI(
    title="Task Manager AI Agent 🚀",
    description="מערכת לניהול משימות חכמה המופעלת על ידי סוכן בינה מלאכותית",
    version="1.0.0"
)

# הוספת הגישה לדפדפנים חיצוניים
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # מאפשר לכל דפדפן להתחבר
    allow_credentials=True,
    allow_methods=["*"], # מאפשר POST, GET, DELETE וכו'
    allow_headers=["*"],
)

# 2. הגדרת המודלים של הנתונים
class ChatRequest(BaseModel):
    message: str

# בדיוק כמו שביקשת - משימה פשוטה עם דבר אחד להכניס
class TaskItem(BaseModel):
    title: str

# --- 3. נקודות קצה לניהול משימות (Todo List Management) ---

@app.get("/tasks", tags=["Tasks Control"])
def list_tasks():
    """מחזיר את רשימת כל המשימות ששמורות במערכת"""
    return todo_service.get_tasks()

@app.post("/tasks", tags=["Tasks Control"])
def add_manual_task(task: TaskItem):
    """מאפשר להוסיף משימה בצורה ידנית (בלי ה-Agent)"""
    result = todo_service.add_task(task.title)
    return {"status": "success", "added_task": result}

@app.delete("/tasks/{task_id}", tags=["Tasks Control"])
def remove_task(task_id: int):
    """מוחק משימה מהרשימה לפי ה-ID שלה"""
    result = todo_service.delete_task(task_id)
    return {"message": result}

# --- 4. נקודת הקצה של הסוכן החכם (AI Agent) ---

@app.post("/chat", tags=["AI Intelligence"])
def chat_with_agent(request: ChatRequest):
    """
    המוח של המערכת: שלחי הודעה חופשית בטקסט
    """
    print(f"User message received: {request.message}")
    
    # הפעלת פונקציית ה-agent מהשירות שכתבנו
    agent_reply = agent_service.agent(request.message)
    
    return {"reply": agent_reply}