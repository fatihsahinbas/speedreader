"""
Storage - SQLite ile okuma ilerlemesi ve istatistik kaydı.
DB_PATH environment variable ile özelleştirilebilir (Docker için).
"""
import os
import sqlite3
from pathlib import Path
from datetime import datetime

# Docker'da /app/data/speedreader.db, lokalde backend/ altında
DB_PATH = Path(os.environ.get("DB_PATH", str(Path(__file__).parent.parent / "speedreader.db")))


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Tabloları oluştur (ilk çalıştırmada)."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                source      TEXT NOT NULL,
                source_type TEXT NOT NULL,
                total_words INTEGER NOT NULL,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS progress (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id    INTEGER NOT NULL,
                mode          TEXT NOT NULL,
                word_position INTEGER DEFAULT 0,
                scroll_pct    REAL DEFAULT 0.0,
                wpm           INTEGER DEFAULT 250,
                updated_at    TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );

            CREATE TABLE IF NOT EXISTS reading_stats (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id   INTEGER NOT NULL,
                mode         TEXT NOT NULL,
                words_read   INTEGER DEFAULT 0,
                duration_sec INTEGER DEFAULT 0,
                avg_wpm      REAL DEFAULT 0.0,
                completed    INTEGER DEFAULT 0,
                finished_at  TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );
        """)

def delete_session(session_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM progress WHERE session_id=?", (session_id,))
        conn.execute("DELETE FROM reading_stats WHERE session_id=?", (session_id,))
        conn.execute("DELETE FROM sessions WHERE id=?", (session_id,))

def create_session(source: str, source_type: str, total_words: int) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO sessions (source, source_type, total_words, created_at) VALUES (?,?,?,?)",
            (source, source_type, total_words, datetime.utcnow().isoformat())
        )
        return cur.lastrowid or 0


def save_progress(session_id: int, mode: str, word_position: int = 0,
                  scroll_pct: float = 0.0, wpm: int = 250):
    now = datetime.utcnow().isoformat()
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM progress WHERE session_id=? AND mode=?",
            (session_id, mode)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE progress SET word_position=?, scroll_pct=?, wpm=?, updated_at=? WHERE session_id=? AND mode=?",
                (word_position, scroll_pct, wpm, now, session_id, mode)
            )
        else:
            conn.execute(
                "INSERT INTO progress (session_id, mode, word_position, scroll_pct, wpm, updated_at) VALUES (?,?,?,?,?,?)",
                (session_id, mode, word_position, scroll_pct, wpm, now)
            )


def get_progress(session_id: int, mode: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM progress WHERE session_id=? AND mode=?",
            (session_id, mode)
        ).fetchone()
        return dict(row) if row else None


def save_stat(session_id: int, mode: str, words_read: int,
              duration_sec: int, completed: bool = False):
    avg_wpm = round((words_read / duration_sec) * 60, 1) if duration_sec > 0 else 0
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO reading_stats (session_id, mode, words_read, duration_sec, avg_wpm, completed, finished_at) VALUES (?,?,?,?,?,?,?)",
            (session_id, mode, words_read, duration_sec, avg_wpm,
             1 if completed else 0,
             datetime.utcnow().isoformat() if completed else None)
        )


def get_all_stats() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT s.source, s.source_type, s.total_words, s.created_at,
                   r.mode, r.words_read, r.duration_sec, r.avg_wpm, r.completed
            FROM reading_stats r
            JOIN sessions s ON s.id = r.session_id
            ORDER BY r.id DESC
        """).fetchall()
        return [dict(r) for r in rows]


def get_recent_sessions(limit: int = 10) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT s.*, p.mode, p.word_position, p.scroll_pct, p.wpm
            FROM sessions s
            LEFT JOIN progress p ON p.session_id = s.id
            ORDER BY s.id DESC LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]


def get_dashboard_summary() -> dict:
    with get_connection() as conn:
        totals = conn.execute("""
            SELECT COUNT(*) as total_sessions,
                   COALESCE(SUM(words_read), 0) as total_words,
                   COALESCE(SUM(duration_sec), 0) as total_seconds,
                   COALESCE(AVG(NULLIF(avg_wpm, 0)), 0) as overall_avg_wpm,
                   COALESCE(SUM(completed), 0) as completed_count
            FROM reading_stats
        """).fetchone()

        modes = conn.execute("""
            SELECT mode, COUNT(*) as cnt, COALESCE(SUM(words_read),0) as words
            FROM reading_stats GROUP BY mode
        """).fetchall()

        daily = conn.execute("""
            SELECT DATE(finished_at) as day,
                   SUM(words_read) as words,
                   SUM(duration_sec) as seconds,
                   ROUND(AVG(NULLIF(avg_wpm,0)), 1) as avg_wpm
            FROM reading_stats
            WHERE finished_at IS NOT NULL
              AND DATE(finished_at) >= DATE('now', '-6 days')
            GROUP BY DATE(finished_at)
            ORDER BY day ASC
        """).fetchall()

        wpm_trend = conn.execute("""
            SELECT avg_wpm, mode, DATE(finished_at) as day
            FROM reading_stats
            WHERE avg_wpm > 0 AND finished_at IS NOT NULL
            ORDER BY id DESC LIMIT 10
        """).fetchall()

        return {
            "totals": dict(totals) if totals else {},
            "modes": [dict(m) for m in modes],
            "daily": [dict(d) for d in daily],
            "wpm_trend": [dict(w) for w in reversed(list(wpm_trend))],
        }


def get_session_with_progress(session_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("""
            SELECT s.*, p.mode, p.word_position, p.scroll_pct, p.wpm as saved_wpm
            FROM sessions s
            LEFT JOIN progress p ON p.session_id = s.id
            WHERE s.id = ? ORDER BY p.updated_at DESC LIMIT 1
        """, (session_id,)).fetchone()
        return dict(row) if row else None
