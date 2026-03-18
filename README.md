# AI Task Manager - Function Calling Agent 🤖

פרויקט סוכן חכם (AI Agent) מבוסס Python שמסוגל לנהל רשימת משימות באופן עצמאי. הסוכן מקבל פקודות בשפה טבעית (עברית/אנגלית), מנתח את בקשת המשתמש בעזרת המודל של OpenAI, ומפעיל פונקציות קוד (Function Calling) כדי לעדכן את בסיס הנתונים מאחורי הקלעים.

## ✨ פיצ'רים מרכזיים
* **הבנת שפה טבעית:** אין צורך בפקודות טכניות. פשוט לכתוב "הוסף משימה", "סיימתי את משימה 1", או "תמחק את המשימה האחרונה".
* **ניהול משימות חכם:** הסוכן תומך בפעולות CRUD מלאות (יצירה, קריאה, עדכון סטטוס ומחיקה).
* **ממשק משתמש (UI):** אפליקציית צ'אט דמוית וואטסאפ מבוססת HTML/JS לתקשורת נוחה מול הסוכן.
* **API מתועד:** שרת מבוסס FastAPI עם ממשק Swagger מובנה.

## 🛠️ טכנולוגיות
* **Python 3**
* **FastAPI & Uvicorn** (בניית שרת ה-API)
* **OpenAI API** (שימוש במודל `gpt-4o-mini` וביכולות Function Calling)
* **HTML/CSS/JS** (צד לקוח)

## 🚀 איך להריץ את הפרויקט המקומי?

### 1. הורדת הפרויקט
```bash
git clone [https://github.com/elisheva413/Function-calling.git](https://github.com/elisheva413/Function-calling.git)
cd Function-calling
```

### 2. יצירת סביבה וירטואלית והתקנת ספריות
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. הגדרת משתני סביבה
יש ליצור קובץ בשם `.env` בתיקייה הראשית של הפרויקט, ולהוסיף לתוכו את מפתח ה-API שלכם מ-OpenAI:
```env
OPENAI_API_KEY=your_api_key_here
```

### 4. הרצת השרת
```bash
python -m uvicorn main:app --reload
```

### 5. שימוש
* **ממשק המשתמש (Chat):** פשוט פתחו את הקובץ `index.html` בדפדפן שלכם כדי להתחיל להתכתב עם הסוכן.
* **ממשק המפתחים (Swagger):** נווטו לכתובת `http://127.0.0.1:8000/docs` כדי לבדוק את נקודות הקצה של ה-API.