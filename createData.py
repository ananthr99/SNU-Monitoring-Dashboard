import os
from dbConfigReader import get_connection


# --------------------------------------------------
# PUBLIC FUNCTION (will be called from app.py)
# --------------------------------------------------
def initialize_views():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        views_dir = os.path.join(base_dir, "views")

        if not os.path.exists(views_dir):
            raise Exception(f"Views folder not found: {views_dir}")

        details_files = ["vwmon_SNUSiteDetailsDaily.sql", "vwmon_SNUSiteDetailsWeekly.sql"]
        count_files = ["vwmon_SNUSiteCountsDaily.sql","vwmon_SNUSiteCountsWeekly.sql"]

        for file in details_files:
            file_path = os.path.join(views_dir, file)
            print(f"Executing: {file}")
            with open(file_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
            cursor.execute(sql_script)
            print(f"SUCCESS: {file}\n")

        for file in count_files:
            file_path = os.path.join(views_dir, file)
            print(f"Executing: {file}")
            with open(file_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
            cursor.execute(sql_script)
            print(f"SUCCESS: {file}\n")

    finally:
        cursor.close()
        conn.close()
