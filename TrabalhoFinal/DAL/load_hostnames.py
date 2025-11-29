import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hostnames.db")
HOSTS_FILE = os.path.join(os.path.dirname(__file__), "hostnames.txt")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS allowed_hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostname TEXT UNIQUE NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def load_hostnames():
    if not os.path.exists(HOSTS_FILE):
        print(f"Hostnames file not found: {HOSTS_FILE}")
        return

    conn = sqlite3.connect(DB_PATH)
    inserted = 0
    skipped = 0

    try:
        cur = conn.cursor()
        with open(HOSTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                hostname = line.strip().lower()
                if not hostname or hostname.startswith("#"):
                    continue
                try:
                    cur.execute(
                        "INSERT OR IGNORE INTO allowed_hosts(hostname) VALUES (?)",
                        (hostname,),
                    )
                    if cur.rowcount > 0:
                        inserted += 1
                    else:
                        skipped += 1
                except sqlite3.Error as e:
                    print(f"Error inserting {hostname}: {e}")
        conn.commit()
    finally:
        conn.close()

    print(f"Inserted {inserted} hostnames, skipped {skipped} (already present).")


if __name__ == "__main__":
    print(f"Using database at: {DB_PATH}")
    init_db()
    load_hostnames()
