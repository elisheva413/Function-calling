# import json
# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# import todo_service 
# import pip_system_certs

# load_dotenv()

# # יוצר חיבור ל-OpenAI באמצעות המפתח שלך
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # הגדרת הכלים: "מילון" שמסביר ל-GPT אילו פונקציות קיימות
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_tasks",
#             "description": "שליפת משימות. אפשר לסנן לפי סטטוס.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "status": {"type": "string", "description": "סטטוס לסינון. למשל: פתוח, בביצוע, בוצע"}
#                 }
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "add_task",
#             "description": "הוספת משימה חדשה למערכת",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "task_id": {"type": "integer", "description": "קוד משימה ייחודי (מספר שלם, אפשר להמציא אם המשתמש לא סיפק)"},
#                     "title": {"type": "string", "description": "כותרת המשימה"},
#                     "description": {"type": "string", "description": "תיאור המשימה"},
#                     "status": {"type": "string", "description": "סטטוס המשימה (ברירת מחדל: פתוח)"}
#                 },
#                 "required": ["task_id", "title"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "update_task",
#             "description": "עדכון סטטוס של משימה קיימת",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "task_id": {"type": "integer", "description": "קוד המשימה שרוצים לעדכן"},
#                     "new_status": {"type": "string", "description": "הסטטוס החדש שצריך לעדכן אליו"}
#                 },
#                 "required": ["task_id", "new_status"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "delete_task",
#             "description": "מחיקת משימה מהמערכת לפי הקוד שלה",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "task_id": {"type": "integer", "description": "קוד המשימה למחיקה"}
#                 },
#                 "required": ["task_id"]
#             }
#         }
#     }
# ]

# def agent(query: str):
#     """
#     מקבלת בקשה מהמשתמש (query), מתייעצת עם GPT, מפעילה פונקציות לפי הצורך, 
#     ומחזירה תשובה אנושית.
#     """
#     messages = [{"role": "user", "content": query}]
    
#     # שולחים ל-GPT את הבקשה יחד עם רשימת הכלים
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages,
#         tools=tools
#     )
    
#     response_message = response.choices[0].message
    
#     # בודקים אם GPT החליט שצריך להפעיל פונקציה
#     if response_message.tool_calls:
#         messages.append(response_message)
        
#         # עוברים על כל הפונקציות ש-GPT ביקש להפעיל
#         for tool_call in response_message.tool_calls:
#             function_name = tool_call.function.name
#             function_args = json.loads(tool_call.function.arguments)
            
#             print(f"Agent is executing: {function_name} with args: {function_args}")
            
#             # מפעילים את הפונקציה המתאימה מקובץ todo_service
#             if function_name == "get_tasks":
#                 function_response = todo_service.get_tasks(**function_args)
#             elif function_name == "add_task":
#                 function_response = todo_service.add_task(**function_args)
#             elif function_name == "update_task":
#                 function_response = todo_service.update_task(**function_args)
#             elif function_name == "delete_task":
#                 function_response = todo_service.delete_task(**function_args)
#             else:
#                 function_response = "Function not found"
            
#             # מחזירים ל-GPT את התוצאה של הפונקציה
#             messages.append({
#                 "tool_call_id": tool_call.id,
#                 "role": "tool",
#                 "name": function_name,
#                 "content": str(function_response),
#             })
        
#         # שולחים שוב ל-GPT כדי שינסח לנו תשובה יפה
#         final_response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages
#         )
#         return final_response.choices[0].message.content
    
#     # אם אין צורך בפונקציות (למשל סתם שיחה רגילה)
#     return response_message.content
# import json
# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# import todo_service 
# import pip_system_certs # חשוב לנטפרי

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_tasks",
#             "description": "שליפת רשימת המשימות הקיימות",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "status": {"type": "string", "description": "סינון לפי סטטוס (פתוח/בוצע)"}
#                 }
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "add_task",
#             "description": "הוספת משימה חדשה למערכת",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "title": {"type": "string", "description": "כותרת המשימה"},
#                     "description": {"type": "string", "description": "תיאור נוסף"},
#                     "status": {"type": "string", "description": "פתוח או בוצע"}
#                 },
#                 "required": ["title"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "update_task",
#             "description": "עדכון סטטוס משימה קיימת",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "task_id": {"type": "integer", "description": "קוד המשימה לעדכון"},
#                     "new_status": {"type": "string", "description": "סטטוס חדש"}
#                 },
#                 "required": ["task_id", "new_status"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "delete_task",
#             "description": "מחיקת משימה לפי קוד",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "task_id": {"type": "integer", "description": "קוד המשימה למחיקה"}
#                 },
#                 "required": ["task_id"]
#             }
#         }
#     }
# ]

# def agent(query: str):
#     messages = [{"role": "user", "content": query}]
#     response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
#     response_message = response.choices[0].message

#     if response_message.tool_calls:
#         messages.append(response_message)
#         for tool_call in response_message.tool_calls:
#             f_name = tool_call.function.name
#             f_args = json.loads(tool_call.function.arguments)
            
#             # הרצת הפונקציה המתאימה
#             func = getattr(todo_service, f_name)
#             f_res = func(**f_args)
            
#             messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": f_name, "content": str(f_res)})
        
#         final_res = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
#         return final_res.choices[0].message.content
#     return response_message.content


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
    messages = [{"role": "user", "content": query}]
    
    # שולחים ל-GPT את הבקשה יחד עם רשימת הכלים
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )
    
    response_message = response.choices[0].message
    
    # בודקים אם GPT החליט שצריך להפעיל פונקציה
    if response_message.tool_calls:
        messages.append(response_message)
        
        # עוברים על כל הפונקציות ש-GPT ביקש להפעיל
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"Agent is executing: {function_name} with args: {function_args}")
            
            # מפעילים את הפונקציה המתאימה מקובץ todo_service
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
            
            # מחזירים ל-GPT את התוצאה של הפונקציה (ממירים ל-string כדי שלא יקרוס)
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response, ensure_ascii=False) if isinstance(function_response, list) else str(function_response),
            })
        
        # שולחים שוב ל-GPT כדי שינסח לנו תשובה יפה
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    # אם אין צורך בפונקציות (למשל סתם שיחה רגילה)
    return response_message.content