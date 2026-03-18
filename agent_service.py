import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import todo_service 
import pip_system_certs

load_dotenv()

# יוצר חיבור ל-OpenAI באמצעות המפתח שלך
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# הגדרת הכלים: "מילון" שמסביר ל-GPT אילו פונקציות קיימות
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "שליפת משימות. אפשר לסנן לפי סטטוס.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "סטטוס לסינון. למשל: פתוח, בוצע"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "הוספת משימה חדשה למערכת",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "כותרת המשימה (מה צריך לעשות)"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "עדכון סטטוס של משימה קיימת",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "קוד המשימה שרוצים לעדכן"},
                    "new_status": {"type": "string", "description": "הסטטוס החדש שצריך לעדכן אליו"}
                },
                "required": ["task_id", "new_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "מחיקת משימה מהמערכת לפי הקוד שלה",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "קוד המשימה למחיקה"}
                },
                "required": ["task_id"]
            }
        }
    }
]

def agent(query: str):
    """
    מקבלת בקשה מהמשתמש (query), מתייעצת עם GPT, מפעילה פונקציות לפי הצורך, 
    ומחזירה תשובה אנושית.
    """
    # --- השדרוג הענק: ה"שליף" ---
    # אנחנו מביאים את המשימות הנוכחיות מהזיכרון
    current_state = todo_service.get_tasks()
    
    # כותבים לו הוראה ברורה מאחורי הקלעים
    system_prompt = f"""
    אתה סוכן חכם לניהול משימות. 
    שים לב! אלו המשימות שקיימות כרגע במסד הנתונים:
    {current_state}
    
    חובה עליך להסתכל ברשימה הזו כדי למצוא את ה-ID המדויק לפני שאתה מוחק או מעדכן משימה.
    אם המשתמש אומר "תמחק את הראשונה", תמצא את המשימה הראשונה ברשימה שסיפקתי לך, ותשתמש ב-ID שלה. אל תנחש מספרים!
    """

    # עכשיו אנחנו שולחים לו קודם את ה"הוראות למפעיל", ורק אז את ההודעה שלך
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    # -----------------------------
    
    # שולחים ל-GPT את הבקשה יחד עם רשימת הכלים (מכאן זה אותו קוד כמו קודם)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )
    
    response_message = response.choices[0].message
    
    if response_message.tool_calls:
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"Agent is executing: {function_name} with args: {function_args}")
            
            if function_name == "get_tasks":
                function_response = todo_service.get_tasks(**function_args)
            elif function_name == "add_task":
                function_response = todo_service.add_task(**function_args)
            elif function_name == "update_task":
                function_response = todo_service.update_task(**function_args)
            elif function_name == "delete_task":
                function_response = todo_service.delete_task(**function_args)
            else:
                function_response = "Function not found"
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response, ensure_ascii=False) if isinstance(function_response, list) else str(function_response),
            })
        
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    return response_message.content