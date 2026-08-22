import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app, g


def get_db():
    if "db" not in g:
        database_url = current_app.config["DATABASE_URL"]

        if database_url.startswith(("postgres://", "postgresql://")):
            g.db = psycopg2.connect(
                database_url,
                cursor_factory=RealDictCursor
            )
        else:
            g.db = sqlite3.connect(database_url)
            g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()
        database_url = current_app.config["DATABASE_URL"]

        postgres_kullaniliyor = database_url.startswith(
            ("postgres://", "postgresql://")
        )

        if postgres_kullaniliyor:
            cursor = db.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id SERIAL PRIMARY KEY,
                    isim TEXT NOT NULL,
                    telefon TEXT NOT NULL,
                    email TEXT NOT NULL,
                    mesaj TEXT,
                    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    durum TEXT DEFAULT 'Yeni'
                )
                """
            )

            cursor.execute(
                """
                ALTER TABLE leads
                ADD COLUMN IF NOT EXISTS durum TEXT DEFAULT 'Yeni'
                """
            )

            cursor.close()

        else:
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

            columns = db.execute(
                "PRAGMA table_info(leads)"
            ).fetchall()

            column_names = [
                column["name"] for column in columns
            ]

            if "durum" not in column_names:
                db.execute(
                    "ALTER TABLE leads "
                    "ADD COLUMN durum TEXT DEFAULT 'Yeni'"
                )

        db.commit()


def lead_ekle(isim, telefon, email, mesaj=None):
    db = get_db()
    database_url = current_app.config["DATABASE_URL"]

    postgres_kullaniliyor = database_url.startswith(
        ("postgres://", "postgresql://")
    )

    if postgres_kullaniliyor:
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO leads (isim, telefon, email, mesaj)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (isim, telefon, email, mesaj),
        )

        lead_id = cursor.fetchone()["id"]
        cursor.close()

    else:
        cursor = db.execute(
            """
            INSERT INTO leads (isim, telefon, email, mesaj)
            VALUES (?, ?, ?, ?)
            """,
            (isim, telefon, email, mesaj),
        )

        lead_id = cursor.lastrowid

    db.commit()

    return lead_id


def tum_leadler():
    db = get_db()
    database_url = current_app.config["DATABASE_URL"]

    postgres_kullaniliyor = database_url.startswith(
        ("postgres://", "postgresql://")
    )

    if postgres_kullaniliyor:
        cursor = db.cursor()

        cursor.execute(
            """
            SELECT id, isim, telefon, email, mesaj, tarih, durum
            FROM leads
            ORDER BY tarih DESC
            """
        )

        leads = cursor.fetchall()
        cursor.close()

    else:
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
    database_url = current_app.config["DATABASE_URL"]

    postgres_kullaniliyor = database_url.startswith(
        ("postgres://", "postgresql://")
    )

    if postgres_kullaniliyor:
        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE leads
            SET durum = %s
            WHERE id = %s
            """,
            (durum, lead_id),
        )

        cursor.close()

    else:
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
    database_url = current_app.config["DATABASE_URL"]

    postgres_kullaniliyor = database_url.startswith(
        ("postgres://", "postgresql://")
    )

    if postgres_kullaniliyor:
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM leads WHERE id = %s",
            (lead_id,)
        )

        silinen_sayi = cursor.rowcount
        cursor.close()

    else:
        cursor = db.execute(
            "DELETE FROM leads WHERE id = ?",
            (lead_id,)
        )

        silinen_sayi = cursor.rowcount

    db.commit()

    return silinen_sayi > 0