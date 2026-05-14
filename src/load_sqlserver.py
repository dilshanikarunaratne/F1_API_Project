from sqlalchemy import create_engine


def get_sqlserver_engine():
    server = "localhost"
    database = "F1_API_Project"

    engine = create_engine(
        f"mssql+pyodbc://@{server}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )

    return engine


def save_to_sqlserver(df, season):
    engine = get_sqlserver_engine()

    table_name = f"f1_results_{season}"

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Saved to SQL Server table: {table_name}")