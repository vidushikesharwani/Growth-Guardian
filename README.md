# 🌱 Growth Guardian

**A comprehensive web-based child healthcare platform for tracking developmental milestones, vaccination schedules, and early detection of developmental delays.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-blue?style=for-the-badge)](https://growth-guardian-q33l.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-red?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)

---

## 🎯 Project Overview

Growth Guardian is designed to help parents especially in remote or low-resource areas: monitor their child's health and development. The platform provides:

- 📊 **Milestone Tracking**: Monitor motor, speech, social and cognitive development
- 💉 **Vaccination Schedules**: Never miss important immunizations with automated reminders
- ⚠️ **Early Alert System**: Detect developmental delays based on WHO standards
- 📈 **Growth Charts**: Visualize height, weight and head circumference trends
- 👨‍⚕️ **Telemedicine Integration**: Book online consultations with pediatricians

**🌐 Live Application:** [https://growth-guardian-q33l.onrender.com/](https://growth-guardian-q33l.onrender.com/)

---

## ✨ Key Features

### 1. Child Profile Management
- Create comprehensive profiles with birth details
- Track multiple children from a single account
- Calculate age automatically for milestone assessment

### 2. Milestone Tracking
- Record developmental milestones across 4 categories:
  - 🏃 Motor Skills (sitting, crawling, walking)
  - 🗣️ Speech & Language (first words, sentences)
  - 🤝 Social & Emotional (smiling, playing with others)
  - 🧠 Cognitive (problem-solving, memory)
- Compare progress against WHO standards
- Risk level detection: Normal, Mild Delay, High Risk

### 3. Vaccination Management
- Pre-loaded Indian immunization schedule
- Track vaccination status (Pending, Completed, Overdue)
- Visual timeline with due dates
- Overdue alerts for missed vaccines

### 4. Pediatric Consultation Booking
- Browse qualified pediatricians
- View doctor profiles with experience and ratings
- Book video consultations
- Paid consultation system (₹450-₹600 per session)

### 5. Dashboard & Analytics
- At-a-glance overview of all children
- Status indicators (All Normal, Mild Delay)
- Quick access to child details and actions

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **ORM**: Raw SQL with sqlite3
- **API Design**: RESTful endpoints

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom styling with gradients and animations
- **Template Engine**: Jinja2

### Deployment
- **Platform**: Render.com
- **Server**: Gunicorn WSGI
- **Storage**: Persistent SQLite database

---

## 📁 Project Structure

```
growth-guardian/
│
├── app.py                      # Main Flask application
├── database.db                 # SQLite database
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── templates/                  # HTML templates (Jinja2)
│   ├── index.html             # Homepage
│   ├── add_child.html         # Child registration form
│   ├── dashboard.html         # Children dashboard
│   ├── child_detail.html      # Individual child view
│   ├── add_milestone.html     # Milestone entry form
│   └── consultation.html      # Doctor booking page
│
├── static/                     # Static assets
│   ├── logo1.png.jpeg         # Application logo
│   └── (future: CSS/JS files)
│
└── .gitignore                 # Git ignore rules
```

---

## 📊 Database Schema

### Tables

#### 1. `children`
Stores child profile information.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Child's full name |
| date_of_birth | DATE | Birth date |
| gender | TEXT | Male/Female |
| birth_weight | REAL | Weight at birth (kg) |
| birth_height | REAL | Height at birth (cm) |
| parent_name | TEXT | Guardian name |
| parent_phone | TEXT | Contact number |
| parent_email | TEXT | Email address |
| created_at | TIMESTAMP | Record creation time |

#### 2. `milestones`
Tracks developmental milestones.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| child_id | INTEGER | Foreign key to children |
| age_months | INTEGER | Child's age when recorded |
| category | TEXT | Motor/Speech/Social/Cognitive |
| milestone_name | TEXT | Specific milestone |
| achieved | BOOLEAN | Yes/No |
| date_recorded | DATE | Recording date |
| risk_level | TEXT | Normal/Mild Delay/High Risk |
| notes | TEXT | Optional observations |

#### 3. `vaccinations`
Manages vaccination schedule.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| child_id | INTEGER | Foreign key to children |
| vaccine_name | TEXT | Vaccine name (e.g., BCG, DPT) |
| due_date | DATE | Scheduled date |
| given_date | DATE | Actual date (if completed) |
| status | TEXT | pending/completed/overdue |
| created_at | TIMESTAMP | Record creation time |

#### 4. `growth_records`
Stores growth measurements.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| child_id | INTEGER | Foreign key to children |
| age_months | INTEGER | Age at measurement |
| weight | REAL | Weight in kg |
| height | REAL | Height in cm |
| head_circumference | REAL | Head size in cm |
| recorded_date | DATE | Measurement date |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vidushikesharwani/Growth-Guardian
   cd Growth-Guardian
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python
   >>> from app import init_db
   >>> init_db()
   >>> exit()
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 🔧 Configuration

### Environment Variables

For production deployment, set these environment variables:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=path-to-database.db
```

### Database Configuration

The app uses SQLite by default. To switch to PostgreSQL (for production):

1. Update `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```

2. Modify `get_db()` in `app.py`:
   ```python
   import psycopg2
   
   def get_db():
       conn = psycopg2.connect(os.environ['DATABASE_URL'])
       return conn
   ```

---

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Purple Gradient Theme**: Professional healthcare aesthetic
- **Interactive Cards**: Hover effects and smooth transitions
- **Tab Navigation**: Child detail page with milestone/vaccination/growth tabs
- **Status Badges**: Color-coded indicators (green/yellow/red)
- **Form Validation**: Client-side and server-side validation

---

## 🔐 Security Features

- Input sanitization on all forms
- SQL injection prevention with parameterized queries
- CSRF protection (to be implemented with Flask-WTF)
- Secure password hashing (for future user authentication)
- Database connection timeout handling

---

## 📈 Future Enhancements

### Planned Features
- [ ] User authentication (login/signup)
- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] SMS/Email notifications for overdue vaccines
- [ ] Growth chart visualization with Chart.js
- [ ] Export reports as PDF
- [ ] Integration with telemedicine platforms
- [ ] Community forum for parents

### Technical Improvements
- [ ] Migrate to PostgreSQL for production
- [ ] Add Redis caching
- [ ] Implement WebSocket for real-time notifications
- [ ] Create REST API for mobile app
- [ ] Add automated testing (pytest)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Docker containerization

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use semantic HTML and BEM methodology for CSS
- Write meaningful commit messages
- Add comments for complex logic
- Test thoroughly before submitting PR

---

## 🐛 Known Issues

- Database lock issue when multiple requests occur simultaneously (fixed with connection timeout)
- Milestone form requires manual child_id input (will be automated)
- Dashboard child cards are initially hardcoded (migrated to dynamic)
- Logo path inconsistency between templates and static folder (resolved)

---

## 📝 API Documentation

### Endpoints

#### **POST** `/api/child`
Create a new child profile.

**Request Body:**
```json
{
  "name": "Aarav Kumar",
  "date_of_birth": "2023-01-15",
  "gender": "Male",
  "parent_email": "parent@example.com"
}
```

**Response:** Redirects to `/dashboard`

---

#### **POST** `/api/milestone`
Record a developmental milestone.

**Request Body:**
```json
{
  "child_id": 1,
  "age_months": 12,
  "category": "Motor",
  "milestone_name": "Walks independently",
  "achieved": "yes",
  "notes": "Walked 5 steps without support"
}
```

**Response:** Redirects to `/child/<child_id>`

---

#### **GET** `/dashboard`
View all children.

**Response:** Renders dashboard with children list.

---

#### **GET** `/child/<int:child_id>`
View individual child details.

**Response:** Renders child detail page with milestones and vaccinations.

---



## 🙏 Acknowledgments

- **WHO Growth Standards**: Milestone comparison data
- **Indian Academy of Pediatrics**: Vaccination schedule
- **Flask Documentation**: Framework guidance
- **Render.com**: Free hosting platform
- **Open-source community**: Inspiration and resources

---

## 👥 Team

**Project developed by:**
- **Person A**: Backend Development (Flask, Database, API)
- **Person B**: Frontend Development (HTML, CSS, JavaScript)

**Course Project:** Web Development & Child Healthcare
**Institution:** [VIT Bhopal University]
**Year:** 2025-2026

---



---

## 📞 Support

For issues, questions, or suggestions:
- **Email**: support@growth-guardian.com
- **GitHub Issues**: [Create an issue](https://github.com/YOUR_USERNAME/growth-guardian/issues)
- **Live Demo**: [https://growth-guardian-q33l.onrender.com/](https://growth-guardian-q33l.onrender.com/)

---

## 🌟 Star this Repository

If you find this project useful, please give it a ⭐ on GitHub!

---

**Made with ❤️ for children's health and development**
