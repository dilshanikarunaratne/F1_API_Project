import sqlite3


def save_to_sqlite(df, season):
    db_path = "C:/Users/Dilshani/Documents/F1_API_Project/data/f1_database.db"

    conn = sqlite3.connect(db_path)

    table_name = f"f1_results_{season}"

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    df.to_sql(
        "f1_results",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    print(f"Saved data to SQLite table: {table_name}")