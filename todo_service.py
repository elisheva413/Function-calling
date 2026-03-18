# import json

# tasks_db = []

# def get_tasks(status=None):
#     """
#     שליפת משימות. אפשר לסנן לפי סטטוס (למשל: 'פתוח', 'בוצע').
#     הפונקציה מחזירה מחרוזת JSON כדי שלסוכן ה-AI יהיה קל לקרוא את התשובה.
#     """
#     if status:
#         filtered_tasks = [task for task in tasks_db if task.get("status") == status]
#         return json.dumps(filtered_tasks, ensure_ascii=False)
    
#     return json.dumps(tasks_db, ensure_ascii=False)

# def add_task(task_id: int, title: str, description: str = "", task_type: str = "", start_date: str = "", end_date: str = "", status: str = "פתוח"):
#     """
#     הוספת משימה חדשה למערך.
#     """
#     new_task = {
#         "id": task_id,
#         "title": title,
#         "description": description,
#         "type": task_type,
#         "start_date": start_date,
#         "end_date": end_date,
#         "status": status
#     }
#     tasks_db.append(new_task)
#     return f"המשימה '{title}' נוספה בהצלחה עם קוד {task_id}."

# def update_task(task_id: int, new_status: str):
#     """
#     עדכון סטטוס של משימה קיימת לפי הקוד שלה.
#     """
#     for task in tasks_db:
#         if task["id"] == task_id:
#             task["status"] = new_status
#             return f"המשימה {task_id} עודכנה בהצלחה לסטטוס החדש: '{new_status}'."
            
#     return f"שגיאה: לא הצלחתי למצוא משימה עם קוד {task_id}."

# def delete_task(task_id: int):
#     """
#     מחיקת משימה מהמערך לפי הקוד שלה.
#     """
#     global tasks_db # אנו משתמשים ב-global כדי לשנות את המערך הראשי
#     initial_length = len(tasks_db)
    
#     # מסננים החוצה את המשימה שאנחנו רוצים למחוק
#     tasks_db = [task for task in tasks_db if task["id"] != task_id]
    
#     if len(tasks_db) < initial_length:
#         return f"המשימה {task_id} נמחקה בהצלחה."
        
#     return f"שגיאה: לא מצאתי משימה עם קוד {task_id} כדי למחוק."
# import json

# tasks_db = []
# # מונה פנימי לייצור ID אוטומטי
# id_counter = 1

# def get_tasks(status=None):
#     """שליפת משימות. מחזיר רשימה (FastAPI כבר יהפוך אותה ל-JSON)"""
#     if status:
#         return [task for task in tasks_db if task.get("status") == status]
#     return tasks_db

# def add_task(title: str, description: str = "", task_type: str = "", start_date: str = "", end_date: str = "", status: str = "פתוח", task_id: int = None):
#     """הוספת משימה חדשה. אם אין ID, מייצר אחד אוטומטית."""
#     global id_counter
    
#     # אם לא קיבלנו ID (מה-Agent או ידנית), נשתמש במונה שלנו
#     actual_id = task_id if task_id is not None else id_counter
#     if task_id is None:
#         id_counter += 1

#     new_task = {
#         "id": actual_id,
#         "title": title,
#         "description": description,
#         "type": task_type,
#         "start_date": start_date,
#         "end_date": end_date,
#         "status": status
#     }
#     tasks_db.append(new_task)
#     return f"המשימה '{title}' נוספה בהצלחה עם קוד {actual_id}."

# def update_task(task_id: int, new_status: str):
#     for task in tasks_db:
#         if task["id"] == task_id:
#             task["status"] = new_status
#             return f"המשימה {task_id} עודכנה לסטטוס: '{new_status}'."
#     return f"שגיאה: לא מצאתי משימה עם קוד {task_id}."

# def delete_task(task_id: int):
#     global tasks_db
#     initial_length = len(tasks_db)
#     tasks_db = [task for task in tasks_db if task["id"] != task_id]
    
#     if len(tasks_db) < initial_length:
#         return f"המשימה {task_id} נמחקה בהצלחה."
#     return f"שגיאה: לא מצאתי משימה עם קוד {task_id}."

import json

tasks_db = []
current_id = 1 # מונה למתן קוד משימה אוטומטי

def get_tasks(status=None):
    """
    שליפת משימות. אפשר לסנן לפי סטטוס.
    """
    if status:
        filtered_tasks = [task for task in tasks_db if task.get("status") == status]
        return filtered_tasks
    
    return tasks_db

def add_task(title: str):
    """
    הוספת משימה פשוטה למערך (רק כותרת). ה-ID נוצר לבד.
    """
    global current_id
    new_task = {
        "id": current_id,
        "title": title,
        "status": "פתוח"
    }
    tasks_db.append(new_task)
    current_id += 1
    return f"המשימה '{title}' נוספה בהצלחה עם קוד {new_task['id']}."

def update_task(task_id: int, new_status: str):
    """
    עדכון סטטוס של משימה קיימת לפי הקוד שלה.
    """
    for task in tasks_db:
        if task["id"] == task_id:
            task["status"] = new_status
            return f"המשימה {task_id} עודכנה בהצלחה לסטטוס החדש: '{new_status}'."
            
    return f"שגיאה: לא הצלחתי למצוא משימה עם קוד {task_id}."

def delete_task(task_id: int):
    """
    מחיקת משימה מהמערך לפי הקוד שלה.
    """
    global tasks_db # אנו משתמשים ב-global כדי לשנות את המערך הראשי
    initial_length = len(tasks_db)
    
    # מסננים החוצה את המשימה שאנחנו רוצים למחוק
    tasks_db = [task for task in tasks_db if task["id"] != task_id]
    
    if len(tasks_db) < initial_length:
        return f"המשימה {task_id} נמחקה בהצלחה."
        
    return f"שגיאה: לא מצאתי משימה עם קוד {task_id} כדי למחוק."