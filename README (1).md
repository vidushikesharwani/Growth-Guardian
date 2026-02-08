# Growth Guardian Backend - Setup Instructions

## 📁 File Structure

Your project should look like this:

```
growth_guardian/
│
├── app.py                  # Main Flask application
├── init_db.py             # Database initialization
├── milestone_checker.py   # WHO milestone logic
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
│
└── templates/            # HTML files (from frontend team)
    ├── index.html
    ├── dashboard.html
    ├── add_child.html
    └── child_detail.html
```

---

## 🚀 STEP-BY-STEP SETUP

### Step 1: Open VS Code
1. Open VS Code
2. Create a new folder called `growth_guardian`
3. Open this folder in VS Code (File → Open Folder)

### Step 2: Create Backend Files
1. Copy all 4 backend files into your folder:
   - `requirements.txt`
   - `init_db.py`
   - `milestone_checker.py`
   - `app.py`

### Step 3: Add Frontend Files
1. Create a folder called `templates` inside `growth_guardian`
2. Put all HTML files from your frontend team in this folder

### Step 4: Install Dependencies

Open VS Code Terminal (View → Terminal) and run:

**For Windows:**
```bash
pip install -r requirements.txt
```

**For Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

### Step 5: Create Database

In the terminal, run:

```bash
python init_db.py
```

You should see:
```
Creating database tables...
✓ Children table created
✓ Milestones table created
✓ Vaccinations table created
✓ Growth records table created

✅ Database initialized successfully!
```

### Step 6: Test Milestone Checker (Optional)

```bash
python milestone_checker.py
```

You should see test results showing the logic works.

### Step 7: Run the Server

```bash
python app.py
```

You should see:
```
🩺 Starting Growth Guardian Backend...
📍 Server running at: http://127.0.0.1:5000
```

### Step 8: Open in Browser

Go to: http://127.0.0.1:5000

You should see your homepage!

---

## 🧪 TESTING THE API

### Test 1: Add a Child

Open a new terminal and run:

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/child -Method POST -ContentType "application/json" -Body '{"name":"Test Baby","date_of_birth":"2024-06-15","gender":"Male","parent_email":"test@email.com"}'
```

**Mac/Linux:**
```bash
curl -X POST http://127.0.0.1:5000/api/child \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Baby","date_of_birth":"2024-06-15","gender":"Male","parent_email":"test@email.com"}'
```

You should get: `{"id":1,"status":"success"}`

### Test 2: Get All Children

```bash
curl http://127.0.0.1:5000/api/children
```

You should see the child you just added!

### Test 3: Add a Milestone

```bash
curl -X POST http://127.0.0.1:5000/api/milestone \
  -H "Content-Type: application/json" \
  -d '{"child_id":1,"category":"motor","milestone_name":"sits_without_support","achieved":false}'
```

---

## 📊 DATABASE VIEWER (Optional but Helpful)

Download **DB Browser for SQLite** to visually see your database:
- Windows/Mac/Linux: https://sqlitebrowser.org/dl/

Open `database.db` with it to see all your data!

---

## 🔧 COMMON ISSUES

### Issue 1: "Module not found: flask"
**Solution:** Run `pip install flask` again

### Issue 2: "Address already in use"
**Solution:** Another app is using port 5000. Change port in app.py:
```python
app.run(debug=True, port=5001)  # Changed to 5001
```

### Issue 3: "Template not found"
**Solution:** Make sure you have a `templates/` folder with HTML files

---

## 📝 NEXT STEPS

1. ✅ Test adding a child through the web form
2. ✅ Test adding milestones
3. ✅ Check if alerts appear
4. ✅ Test vaccination schedule
5. ✅ Add growth records and view chart

---

## 🎯 API ENDPOINTS REFERENCE

### Children
- `POST /api/child` - Add new child
- `GET /api/children` - Get all children
- `GET /api/child/<id>` - Get one child

### Milestones
- `POST /api/milestone` - Add milestone
- `GET /api/child/<id>/milestones` - Get child's milestones
- `GET /api/milestones/available` - Get WHO standards

### Vaccinations
- `GET /api/child/<id>/vaccinations` - Get vaccine schedule
- `POST /api/vaccination/mark-given` - Mark vaccine as done

### Growth
- `POST /api/growth` - Add weight/height
- `GET /api/child/<id>/growth` - Get growth history

### Alerts
- `GET /api/child/<id>/alerts` - Get all alerts

---

## 💡 TIPS

1. Keep the terminal open while testing - you'll see all requests
2. Use `Ctrl+C` to stop the server
3. Any code changes → Save file → Server auto-restarts (in debug mode)
4. Check terminal for error messages if something doesn't work

---

Good luck! 🚀
