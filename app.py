from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import sqlite3
from datetime import datetime, date, timedelta
from milestone_checker import check_milestone_status, get_all_milestones, get_milestones_for_age

app = Flask(__name__)
CORS(app)

# ===== DATABASE HELPER =====
def get_db():
    """Get database connection"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_age_months(date_of_birth):
    """Calculate age in months from date of birth"""
    if isinstance(date_of_birth, str):
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    else:
        dob = date_of_birth
    
    today = date.today()
    months = (today.year - dob.year) * 12 + (today.month - dob.month)
    return months

def calculate_age_details(date_of_birth):
    """Calculate age in years and months separately"""
    if isinstance(date_of_birth, str):
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    else:
        dob = date_of_birth
    
    today = date.today()
    total_months = (today.year - dob.year) * 12 + (today.month - dob.month)
    years = total_months // 12
    months = total_months % 12
    
    return {
        'total_months': total_months,
        'age_years': years,
        'age_months': months
    }

# ===== ROUTES (WEB PAGES) =====

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/home')
def home():
    """Homepage alias"""
    return render_template('index.html')

@app.route('/consultation')
def consultation():
    """Consultation booking page"""
    return render_template('consultation.html')

# ✅ FIXED: Added alias for HTML compatibility
@app.route('/child/<int:child_id>/add_milestone')
def add_milestone_page(child_id):
    """Add milestone page for specific child"""
    conn = get_db()
    child = conn.execute('SELECT * FROM children WHERE id = ?', (child_id,)).fetchone()
    conn.close()
    
    if not child:
        return "Child not found", 404
    
    return render_template('add_milestone.html', child=dict(child), child_id=child_id)

# ✅ FIXED: Added shorter route name for url_for compatibility
@app.route('/add-milestone/<int:child_id>')
def api_add_milestone_page(child_id):
    """Alias route for add milestone"""
    return add_milestone_page(child_id)

@app.route('/dashboard')
def dashboard():
    """Dashboard showing all children"""
    conn = get_db()
    children = conn.execute('SELECT * FROM children ORDER BY created_at DESC').fetchall()
    conn.close()
    
    children_list = []
    for child in children:
        child_dict = dict(child)
        age_info = calculate_age_details(child['date_of_birth'])
        child_dict.update(age_info)
        children_list.append(child_dict)
    
    return render_template('dashboard.html', children=children_list)

@app.route('/add_child')
def add_child():
    """Page to add a new child"""
    return render_template('add_child.html')

@app.route('/child/<int:child_id>')
def child_detail(child_id):
    """Detailed view of a child"""
    conn = get_db()
    
    child = conn.execute('SELECT * FROM children WHERE id = ?', (child_id,)).fetchone()
    if not child:
        conn.close()
        return "Child not found", 404
    
    child_dict = dict(child)
    # ✅ FIXED: Add detailed age calculation
    age_info = calculate_age_details(child['date_of_birth'])
    child_dict.update(age_info)
    
    milestones = conn.execute('''
        SELECT * FROM milestones 
        WHERE child_id = ? 
        ORDER BY date_recorded DESC
    ''', (child_id,)).fetchall()
    
    vaccinations = conn.execute('''
        SELECT * FROM vaccinations 
        WHERE child_id = ? 
        ORDER BY due_date
    ''', (child_id,)).fetchall()
    
    growth = conn.execute('''
        SELECT * FROM growth_records 
        WHERE child_id = ? 
        ORDER BY age_months
    ''', (child_id,)).fetchall()
    
    alerts = get_alerts_for_child(child_id)
    
    conn.close()
    
    return render_template('child_detail.html', 
                         child=child_dict, 
                         milestones=milestones,
                         vaccinations=vaccinations,
                         growth=growth,
                         alerts=alerts,
                         today=date.today())

# ===== API ENDPOINTS =====

@app.route('/api/children', methods=['GET'])
def api_get_children():
    """Get all children"""
    conn = get_db()
    children = conn.execute('SELECT * FROM children ORDER BY created_at DESC').fetchall()
    conn.close()
    
    children_list = []
    for child in children:
        child_dict = dict(child)
        age_info = calculate_age_details(child['date_of_birth'])
        child_dict.update(age_info)
        children_list.append(child_dict)
    
    return jsonify(children_list)

@app.route('/api/child', methods=['POST'])
def api_add_child():
    """Add a new child"""
    data = request.form
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Insert child
        cursor.execute('''
            INSERT INTO children (name, date_of_birth, gender, parent_email, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['name'], data['date_of_birth'], data['gender'], 
              data.get('parent_email', ''), datetime.now()))
        
        child_id = cursor.lastrowid
        
        # Create vaccinations
        if isinstance(data['date_of_birth'], str):
            dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        else:
            dob = data['date_of_birth']
        
        vaccines = [
            ("BCG", 0),
            ("Hepatitis B - Birth dose", 0),
            ("OPV - 0", 0),
            ("DTaP - 1st dose", 6),
            ("IPV - 1st dose", 6),
            ("Hib - 1st dose", 6),
            ("Hepatitis B - 1st dose", 6),
            ("Rotavirus - 1st dose", 6),
            ("DTaP - 2nd dose", 10),
            ("IPV - 2nd dose", 10),
            ("Hib - 2nd dose", 10),
            ("Rotavirus - 2nd dose", 10),
            ("DTaP - 3rd dose", 14),
            ("IPV - 3rd dose", 14),
            ("Hib - 3rd dose", 14),
            ("Hepatitis B - 2nd dose", 14),
            ("Rotavirus - 3rd dose", 14),
            ("MMR - 1st dose", 36),
            ("Typhoid", 36),
            ("MMR - 2nd dose", 60),
            ("Varicella - 1st dose", 60),
            ("DTaP Booster", 72),
            ("IPV Booster", 72),
        ]
        
        for vaccine_name, weeks in vaccines:
            due_date = dob + timedelta(weeks=weeks)
            cursor.execute('''
                INSERT INTO vaccinations (child_id, vaccine_name, due_date, status)
                VALUES (?, ?, ?, 'pending')
            ''', (child_id, vaccine_name, due_date))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return f"Error adding child: {e}", 500
    finally:
        conn.close()
    
    return redirect('/dashboard')

@app.route('/api/child/<int:child_id>', methods=['GET'])
def api_get_child(child_id):
    """Get specific child details"""
    conn = get_db()
    child = conn.execute('SELECT * FROM children WHERE id = ?', (child_id,)).fetchone()
    conn.close()
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404
    
    child_dict = dict(child)
    age_info = calculate_age_details(child['date_of_birth'])
    child_dict.update(age_info)
    
    return jsonify(child_dict)

@app.route('/api/milestone', methods=['POST'])
def api_add_milestone():
    """Add a milestone record"""
    data = request.form
    
    child_id = int(data['child_id'])
    achieved = data.get('achieved') == 'yes'
    
    conn = sqlite3.connect('database.db', timeout=10.0)
    conn.row_factory = sqlite3.Row
    
    try:
        child = conn.execute('SELECT date_of_birth FROM children WHERE id = ?', 
                            (child_id,)).fetchone()
        
        if not child:
            return "Child not found", 404
        
        age_months = calculate_age_months(child['date_of_birth'])
        
        risk_level = check_milestone_status(
            data['category'],
            data['milestone_name'],
            age_months,
            achieved
        )
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO milestones 
            (child_id, age_months, category, milestone_name, achieved, date_recorded, risk_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (child_id, age_months, data['category'], data['milestone_name'],
              achieved, date.today(), risk_level))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return f"Error adding milestone: {e}", 500
    finally:
        conn.close()
    
    return redirect(f'/child/{child_id}')

@app.route('/api/milestones/available', methods=['GET'])
def api_get_available_milestones():
    """Get all available milestones from WHO standards"""
    return jsonify(get_all_milestones())

# ----- VACCINATION APIs -----

@app.route('/api/child/<int:child_id>/vaccinations', methods=['GET'])
def api_get_vaccinations(child_id):
    """Get vaccination schedule for a child"""
    conn = get_db()
    vaccines = conn.execute('''
        SELECT * FROM vaccinations 
        WHERE child_id = ? 
        ORDER BY due_date
    ''', (child_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(v) for v in vaccines])

# ✅ FIXED: Accept both JSON and form data
@app.route('/api/vaccination/mark-given', methods=['POST'])
def api_mark_vaccination():
    """Mark a vaccination as given"""
    # Try JSON first, fallback to form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    
    conn = get_db()
    
    try:
        conn.execute('''
            UPDATE vaccinations 
            SET status = 'completed', given_date = ?
            WHERE id = ?
        ''', (data.get('given_date', str(date.today())), data['vaccination_id']))
        conn.commit()
        
        return jsonify({'status': 'success', 'message': 'Vaccination marked as completed'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/growth', methods=['POST'])
def api_add_growth_record():
    """Add growth record (weight/height)"""
    data = request.form
    
    conn = get_db()
    child = conn.execute('SELECT date_of_birth FROM children WHERE id = ?', 
                        (data['child_id'],)).fetchone()
    
    if not child:
        conn.close()
        return jsonify({'error': 'Child not found'}), 404
    
    age_months = calculate_age_months(child['date_of_birth'])
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO growth_records 
        (child_id, age_months, weight_kg, height_cm, date_recorded)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['child_id'], age_months, data['weight_kg'], 
          data['height_cm'], date.today()))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': record_id, 'status': 'success'})

@app.route('/api/child/<int:child_id>/growth', methods=['GET'])
def api_get_growth_records(child_id):
    """Get growth history for a child"""
    conn = get_db()
    records = conn.execute('''
        SELECT * FROM growth_records 
        WHERE child_id = ? 
        ORDER BY age_months
    ''', (child_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(r) for r in records])

def get_alerts_for_child(child_id):
    """Check for alerts for a specific child"""
    alerts = []
    conn = get_db()
    
    high_risk = conn.execute('''
        SELECT category, milestone_name, age_months FROM milestones
        WHERE child_id = ? AND risk_level = 'high_risk'
    ''', (child_id,)).fetchall()
    
    for m in high_risk:
        alerts.append({
            "type": "milestone_delay",
            "severity": "high",
            "message": f"⚠️ HIGH RISK: {m['milestone_name']} not achieved (expected by {m['age_months']} months)",
            "category": m['category']
        })
    
    mild_delays = conn.execute('''
        SELECT category, milestone_name, age_months FROM milestones
        WHERE child_id = ? AND risk_level = 'mild_delay'
    ''', (child_id,)).fetchall()
    
    for m in mild_delays:
        alerts.append({
            "type": "milestone_delay",
            "severity": "medium",
            "message": f"⚡ MILD DELAY: {m['milestone_name']} - monitor closely",
            "category": m['category']
        })
    
    today = date.today()
    overdue_vaccines = conn.execute('''
        SELECT vaccine_name, due_date FROM vaccinations
        WHERE child_id = ? AND status = 'pending' AND due_date < ?
    ''', (child_id, today)).fetchall()
    
    for v in overdue_vaccines:
        days_overdue = (today - date.fromisoformat(v['due_date'])).days
        severity = "high" if days_overdue > 30 else "medium"
        alerts.append({
            "type": "vaccine_overdue",
            "severity": severity,
            "message": f"💉 VACCINE OVERDUE: {v['vaccine_name']} (due: {v['due_date']}, {days_overdue} days overdue)"
        })
    
    upcoming_date = today + timedelta(days=7)
    upcoming_vaccines = conn.execute('''
        SELECT vaccine_name, due_date FROM vaccinations
        WHERE child_id = ? AND status = 'pending' 
        AND due_date >= ? AND due_date <= ?
    ''', (child_id, today, upcoming_date)).fetchall()
    
    for v in upcoming_vaccines:
        alerts.append({
            "type": "vaccine_reminder",
            "severity": "low",
            "message": f"📅 UPCOMING: {v['vaccine_name']} due on {v['due_date']}"
        })
    
    growth_records = conn.execute('''
        SELECT weight_kg, age_months FROM growth_records
        WHERE child_id = ?
        ORDER BY age_months DESC
        LIMIT 2
    ''', (child_id,)).fetchall()
    
    if len(growth_records) == 2:
        weight_change = growth_records[0]['weight_kg'] - growth_records[1]['weight_kg']
        if weight_change <= 0:
            alerts.append({
                "type": "growth_concern",
                "severity": "medium",
                "message": f"📉 GROWTH CONCERN: No weight gain or weight loss detected"
            })
    
    conn.close()
    return alerts

@app.route('/api/child/<int:child_id>/alerts', methods=['GET'])
def api_get_alerts(child_id):
    """Get all alerts for a child"""
    alerts = get_alerts_for_child(child_id)
    return jsonify(alerts)

# ===== RUN APP =====

if __name__ == '__main__':
    print("🩺 Starting Growth Guardian Backend...")
    print("📍 Server running at: http://127.0.0.1:5000")
    print("\nAvailable endpoints:")
    print("  Web Pages:")
    print("    GET  /                    - Homepage")
    print("    GET  /dashboard           - Dashboard")
    print("    GET  /add_child           - Add child form")
    print("    GET  /child/<id>          - Child details")
    print("    GET  /child/<id>/add_milestone - Add milestone form")
    print("\n  API Endpoints:")
    print("    POST /api/child           - Add child")
    print("    GET  /api/children        - Get all children")
    print("    POST /api/milestone       - Add milestone")
    print("    POST /api/vaccination/mark-given - Mark vaccine as given")
    print("    GET  /api/child/<id>/vaccinations - Get vaccinations")
    print("\n")
    
    app.run(debug=True, port=5000)