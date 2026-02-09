from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime, date, timedelta
from milestone_checker import check_milestone_status, get_all_milestones, get_milestones_for_age

app = Flask(__name__)
CORS(app)  # Allow frontend to make requests

# ===== DATABASE HELPER =====
def get_db():
    """Get database connection"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
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


@app.route('/child/<int:child_id>/add_milestone')
def add_milestone_page(child_id):
    """Add milestone page for specific child"""
    conn = get_db()
    child = conn.execute('SELECT * FROM children WHERE id = ?', (child_id,)).fetchone()
    conn.close()
    
    if not child:
        return "Child not found", 404
    
    return render_template('add_milestone.html', child=dict(child))


@app.route('/dashboard')
def dashboard():
    """Dashboard showing all children"""
    conn = get_db()
    children = conn.execute('SELECT * FROM children ORDER BY created_at DESC').fetchall()
    conn.close()
    
    # Convert to list of dicts and add age
    children_list = []
    for child in children:
        child_dict = dict(child)
        child_dict['age_months'] = calculate_age_months(child['date_of_birth'])
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
    
    # Get child info
    child = conn.execute('SELECT * FROM children WHERE id = ?', (child_id,)).fetchone()
    if not child:
        conn.close()
        return "Child not found", 404
    
    child_dict = dict(child)
    child_dict['age_months'] = calculate_age_months(child['date_of_birth'])
    
    # Get milestones
    milestones = conn.execute('''
        SELECT * FROM milestones 
        WHERE child_id = ? 
        ORDER BY date_recorded DESC
    ''', (child_id,)).fetchall()
    
    # Get vaccinations
    vaccinations = conn.execute('''
        SELECT * FROM vaccinations 
        WHERE child_id = ? 
        ORDER BY due_date
    ''', (child_id,)).fetchall()
    
    # Get growth records
    growth = conn.execute('''
        SELECT * FROM growth_records 
        WHERE child_id = ? 
        ORDER BY age_months
    ''', (child_id,)).fetchall()
    
    # Get alerts
    alerts = get_alerts_for_child(child_id)
    
    conn.close()
    
    return render_template('child_detail.html', 
                         child=child_dict, 
                         milestones=milestones,
                         vaccinations=vaccinations,
                         growth=growth,
                         alerts=alerts)


# ===== API ENDPOINTS =====

# ----- CHILDREN APIs -----

@app.route('/api/children', methods=['GET'])
def api_get_children():
    """Get all children"""
    conn = get_db()
    children = conn.execute('SELECT * FROM children ORDER BY created_at DESC').fetchall()
    conn.close()
    
    children_list = []
    for child in children:
        child_dict = dict(child)
        child_dict['age_months'] = calculate_age_months(child['date_of_birth'])
        children_list.append(child_dict)
    
    return jsonify(children_list)


@app.route('/api/child', methods=['POST'])
def api_add_child():
    """Add a new child"""
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO children (name, date_of_birth, gender, parent_email, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['date_of_birth'], data['gender'], 
          data['parent_email'], datetime.now()))
    
    child_id = cursor.lastrowid
    
    # Auto-generate vaccination schedule for this child
    create_vaccination_schedule(child_id, data['date_of_birth'])
    
    conn.commit()
    conn.close()
    
    return jsonify({'id': child_id, 'status': 'success'})


@app.route('/api/child/<int:child_id>', methods=['GET'])
def api_get_child(child_id):
    """Get specific child details"""
    conn = get_db()
    child = conn.execute('SELECT * FROM children WHERE id = ?', (child_id,)).fetchone()
    conn.close()
    
    if not child:
        return jsonify({'error': 'Child not found'}), 404
    
    child_dict = dict(child)
    child_dict['age_months'] = calculate_age_months(child['date_of_birth'])
    
    return jsonify(child_dict)


# ----- MILESTONE APIs -----

@app.route('/api/milestone', methods=['POST'])
def api_add_milestone():
    """Add a milestone record"""
    data = request.json
    
    # Get child's age
    conn = get_db()
    child = conn.execute('SELECT date_of_birth FROM children WHERE id = ?', 
                        (data['child_id'],)).fetchone()
    
    if not child:
        conn.close()
        return jsonify({'error': 'Child not found'}), 404
    
    age_months = calculate_age_months(child['date_of_birth'])
    
    # Check milestone status
    risk_level = check_milestone_status(
        data['category'],
        data['milestone_name'],
        age_months,
        data['achieved']
    )
    
    # Save to database
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO milestones 
        (child_id, age_months, category, milestone_name, achieved, date_recorded, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['child_id'], age_months, data['category'], data['milestone_name'],
          data['achieved'], date.today(), risk_level))
    
    milestone_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'id': milestone_id,
        'risk_level': risk_level,
        'status': 'success'
    })


@app.route('/api/child/<int:child_id>/milestones', methods=['GET'])
def api_get_milestones(child_id):
    """Get all milestones for a child"""
    conn = get_db()
    milestones = conn.execute('''
        SELECT * FROM milestones 
        WHERE child_id = ? 
        ORDER BY date_recorded DESC
    ''', (child_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(m) for m in milestones])


@app.route('/api/milestones/available', methods=['GET'])
def api_get_available_milestones():
    """Get all available milestones from WHO standards"""
    return jsonify(get_all_milestones())


# ----- VACCINATION APIs -----

def create_vaccination_schedule(child_id, date_of_birth):
    """Create vaccination schedule for a new child"""
    if isinstance(date_of_birth, str):
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    else:
        dob = date_of_birth
    
    # Indian vaccination schedule
    vaccines = [
        ("BCG", 0),
        ("Hepatitis B - Birth dose", 0),
        ("OPV - 0", 0),
        ("DTaP - 1st dose", 6),  # 6 weeks
        ("IPV - 1st dose", 6),
        ("Hib - 1st dose", 6),
        ("Hepatitis B - 1st dose", 6),
        ("Rotavirus - 1st dose", 6),
        ("DTaP - 2nd dose", 10),  # 10 weeks
        ("IPV - 2nd dose", 10),
        ("Hib - 2nd dose", 10),
        ("Rotavirus - 2nd dose", 10),
        ("DTaP - 3rd dose", 14),  # 14 weeks
        ("IPV - 3rd dose", 14),
        ("Hib - 3rd dose", 14),
        ("Hepatitis B - 2nd dose", 14),
        ("Rotavirus - 3rd dose", 14),
        ("MMR - 1st dose", 36),  # 9 months (36 weeks)
        ("Typhoid", 36),
        ("MMR - 2nd dose", 60),  # 15 months
        ("Varicella - 1st dose", 60),
        ("DTaP Booster", 72),  # 18 months
        ("IPV Booster", 72),
    ]
    
    conn = get_db()
    cursor = conn.cursor()
    
    for vaccine_name, weeks in vaccines:
        due_date = dob + timedelta(weeks=weeks)
        cursor.execute('''
            INSERT INTO vaccinations (child_id, vaccine_name, due_date, status)
            VALUES (?, ?, ?, 'pending')
        ''', (child_id, vaccine_name, due_date))
    
    conn.commit()
    conn.close()


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


@app.route('/api/vaccination/mark-given', methods=['POST'])
def api_mark_vaccination():
    """Mark a vaccination as given"""
    data = request.json
    
    conn = get_db()
    conn.execute('''
        UPDATE vaccinations 
        SET status = 'completed', given_date = ?
        WHERE id = ?
    ''', (data.get('given_date', date.today()), data['vaccination_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})


# ----- GROWTH TRACKING APIs -----

@app.route('/api/growth', methods=['POST'])
def api_add_growth_record():
    """Add growth record (weight/height)"""
    data = request.json
    
    # Get child's age
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


# ----- ALERT SYSTEM -----

def get_alerts_for_child(child_id):
    """
    Check for alerts for a specific child
    Returns list of alert objects
    """
    alerts = []
    conn = get_db()
    
    # 1. Check for high-risk milestones
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
    
    # 2. Check for mild delays
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
    
    # 3. Check for overdue vaccinations
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
    
    # 4. Check upcoming vaccinations (within 7 days)
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
    
    # 5. Check for growth concerns
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
    print("\n  API Endpoints:")
    print("    POST /api/child           - Add child")
    print("    GET  /api/children        - Get all children")
    print("    POST /api/milestone       - Add milestone")
    print("    GET  /api/child/<id>/milestones - Get milestones")
    print("    POST /api/growth          - Add growth record")
    print("    GET  /api/child/<id>/alerts - Get alerts")
    print("\n")
    
    app.run(debug=True, port=5000)