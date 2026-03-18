import json

tasks_db = []
current_id = 1 

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