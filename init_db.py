import sqlite3

def init_database():
    """Initialize the database with all required tables"""
    
    # Connect to database (creates it if doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # 1. CHILDREN TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            gender TEXT NOT NULL,
            parent_email TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )
    ''')
    print("✓ Children table created")
    
    # 2. MILESTONES TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            age_months INTEGER NOT NULL,
            category TEXT NOT NULL,
            milestone_name TEXT NOT NULL,
            achieved BOOLEAN NOT NULL,
            date_recorded DATE NOT NULL,
            risk_level TEXT,
            FOREIGN KEY (child_id) REFERENCES children(id)
        )
    ''')
    print("✓ Milestones table created")
    
    # 3. VACCINATIONS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            vaccine_name TEXT NOT NULL,
            due_date DATE NOT NULL,
            given_date DATE,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (child_id) REFERENCES children(id)
        )
    ''')
    print("✓ Vaccinations table created")
    
    # 4. GROWTH RECORDS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS growth_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            age_months INTEGER NOT NULL,
            weight_kg FLOAT NOT NULL,
            height_cm FLOAT NOT NULL,
            date_recorded DATE NOT NULL,
            FOREIGN KEY (child_id) REFERENCES children(id)
        )
    ''')
    print("✓ Growth records table created")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database initialized successfully!")
    print("Database file: database.db")

if __name__ == '__main__':
    init_database()
