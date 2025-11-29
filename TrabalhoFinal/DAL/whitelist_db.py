import os
import sqlite3
from typing import List, Tuple


DB_PATH = os.path.join(os.path.dirname(__file__), "hostnames.db")


class WhitelistDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _query(self, sql: str, params: Tuple = ()) -> list[tuple]:
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()
            conn.commit()
            return rows
        finally:
            conn.close()

    def exact_matches(self, hostname: str) -> List[str]:
        rows = self._query(
            "SELECT hostname FROM allowed_hosts WHERE hostname = ?",
            (hostname,),
        )
        return [r[0] for r in rows]

    def suffix_matches(self, domain: str, limit: int | None = 20) -> List[str]:
        """
        domain: e.g. "example.com" for a query like "*.example.com"
        """
        pattern = "%." + domain
        rows = self._query(
            "SELECT hostname FROM allowed_hosts WHERE hostname LIKE ?",
            (pattern,),
        )
        if limit is not None:
            rows = rows[:limit]
        return [r[0] for r in rows]

