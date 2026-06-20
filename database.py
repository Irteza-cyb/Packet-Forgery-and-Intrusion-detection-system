import sqlite3

DB_NAME = "scapyshield.db"

def get_db_connection():
    """
    Creates and returns a thread-safe connection to the SQLite database
    configured with a high-concurrency timeout and WAL journaling mode.
    """
    # 1. timeout=30.0 lets the sniffer or GUI wait up to 30s for an existing lock to clear
    # 2. check_same_thread=False allows background sniffing threads to execute safely
    conn = sqlite3.connect(DB_NAME, timeout=30.0, check_same_thread=False)
    
    # 🚀 WAL MODE: Allows simultaneous reading (GUI) and writing (Sniffer) without collisions!
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    """Creates one simple table for logs with timestamp."""
    conn = get_db_connection()
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
    cursor.close()  # Clear cursor resources explicitly
    conn.close()
    print("[+] Database created successfully with WAL mode enabled.")


def log_attack(attacker_ip, target_port, attack_type):
    """Inserts a single log entry into the table with timestamp."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Safe insertion using parameterized queries
        cursor.execute(
            "INSERT INTO attack_logs (attacker_ip, target_port, attack_type) VALUES (?, ?, ?)",
            (attacker_ip, target_port, attack_type)
        )
        conn.commit()
        print(f"[+] Logged: {attacker_ip} on port {target_port}")
    except sqlite3.OperationalError as e:
        print(f"[-] Database operation failed: {e}")
    finally:
        cursor.close()  # Ensure resources drop immediately even on failure
        conn.close()


# Test it locally (Fixed the main string naming issue)
if __name__ == "__main__":
    init_db()
    log_attack("192.168.1.15", 22, "SYN Scan")


