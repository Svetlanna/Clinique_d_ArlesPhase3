"""
Helpers partagés par les wrappers CLI headless (resultats_nuit_cli.py,
comorbidites_cli.py, dashboard_cli.py). Pas de dépendance à Streamlit :
ces scripts sont appelés en sous-processus par l'Api Node et doivent
juste imprimer du JSON sur stdout.
"""

import json
import os
import sys
from pathlib import Path

import mysql.connector
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SQLITE_PATH = BASE_DIR / "base_analytique.db"
print(SQLITE_PATH)
NUITS_DIR = BASE_DIR / "nuits"


def mysql_config():
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": int(os.environ.get("DB_PORT", 3306)),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", "root"),
        "database": os.environ.get("DB_NAME", "cliniquearles"),
        "charset": "utf8mb4",
        "use_unicode": True,
    }


def mysql_conn():
    return mysql.connector.connect(**mysql_config())


def sqlite_conn():
    conn = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def df_records(df):
    """DataFrame -> liste de dict JSON-safe (NaN/dates gérés par pandas)."""
    if df is None or df.empty:
        return []
    return json.loads(df.to_json(orient="records", date_format="iso"))


def print_result(result):
    print(json.dumps(result, ensure_ascii=False))


def fail(message):
    print(json.dumps({"error": str(message)}, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)
