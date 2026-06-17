import sqlite3

DB_NAME = "scapyshield.db"

def init_db():
    """Creates one simple table for logs with timestamp."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table with basic columns + timestamp
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attack_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        attacker_ip TEXT,
        target_port INTEGER,
        attack_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    conn.close()
    print("[+] Database created successfully.")


def log_attack(attacker_ip, target_port, attack_type):
    """Inserts a single log entry into the table with timestamp."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Safe insertion using parameterized queries
    cursor.execute(
        "INSERT INTO attack_logs (attacker_ip, target_port, attack_type) VALUES (?, ?, ?)",
        (attacker_ip, target_port, attack_type)
    )
    
    conn.commit()
    conn.close()
    print(f"[+] Logged: {attacker_ip} on port {target_port}")


# Test it locally
if __name__ == "_main_":
    init_db()
    log_attack("192.168.1.15", 22, "SYN Scan")   ### Member 4: The Database Admin (Database Lead)



