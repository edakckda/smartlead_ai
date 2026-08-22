import sqlite3
from flask import current_app, g


def get_db():
    if "db" not in g:
        database_url = current_app.config["DATABASE_URL"]

        g.db = sqlite3.connect(database_url)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                email TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                durum TEXT DEFAULT 'Yeni'
            )
            """
        )
    columns = db.execute("PRAGMA table_info(leads)").fetchall()
    column_names = [column["name"] for column in columns]

    if "durum" not in column_names:
        db.execute(
            "ALTER TABLE leads ADD COLUMN durum TEXT DEFAULT 'Yeni'"
        )
    db.commit()

    app.teardown_appcontext(close_db)


def lead_ekle(isim, telefon, email, mesaj=None):
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO leads (isim, telefon, email, mesaj)
        VALUES (?, ?, ?, ?)
        """,
        (isim, telefon, email, mesaj),
    )

    db.commit()

    return cursor.lastrowid


def tum_leadler():
    db = get_db()

    leads = db.execute(
        """
        SELECT id, isim, telefon, email, mesaj, tarih, durum
        FROM leads
        ORDER BY tarih DESC
        """
    ).fetchall()

    return [dict(lead) for lead in leads]

def lead_durum_guncelle(lead_id, durum):
    db = get_db()

    db.execute(
        """
        UPDATE leads
        SET durum = ?
        WHERE id = ?
        """,
        (durum, lead_id),
    )

    db.commit()

def lead_sil(lead_id):
    db = get_db()

    cursor = db.execute(
        "DELETE FROM leads WHERE id = ?",
        (lead_id,)
    )

    db.commit()

    return cursor.rowcount > 0