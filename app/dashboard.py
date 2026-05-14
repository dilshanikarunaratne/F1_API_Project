import os
import pandas as pd
import streamlit as st
import plotly.express as px
import sys
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

sys.path.append(SRC_DIR)

from extract import get_race_results
from transform import clean_race_results
from load import save_to_sqlite

def load_from_sqlite(season):
    db_path = "C:/Users/Dilshani/Documents/F1_API_Project/data/f1_database.db"
    table_name = f"f1_results_{season}"

    conn = sqlite3.connect(db_path)

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

st.title("F1 Race Results Dashboard")

season = st.selectbox(
    "Select season",
    [2024, 2023, 2022, 2021, 2020],
    index=0
)

if st.button("Load Season Data"):

    df_raw = get_race_results(season)
    df_cleaned = clean_race_results(df_raw)

    raw_path = f"C:/Users/Dilshani/Documents/F1_API_Project/data/raw/f1_results_{season}_raw.csv"
    processed_path = f"C:/Users/Dilshani/Documents/F1_API_Project/data/processed/f1_results_{season}_clean.csv"

    df_raw.to_csv(raw_path, index=False)
    df_cleaned.to_csv(processed_path, index=False)

    save_to_sqlite(df_cleaned, season)

    df_clean = load_from_sqlite(season)

    st.success(f"{season} data loaded and saved successfully.")

    st.dataframe(df_clean)

    

    # KPI cards
    total_races = df_clean["race_name"].nunique()
    total_drivers = df_clean["driver_name"].nunique()
    total_constructors = df_clean["constructor"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Races", total_races)
    col2.metric("Total Drivers", total_drivers)
    col3.metric("Total Constructors", total_constructors)

    st.divider()

    # Segment distribution
    st.subheader("Race Wins by Constructor")

    # Filter only race winners
    winner_df = df_clean[df_clean["position"] == 1]

    # Count wins by constructor
    constructor_wins = winner_df["constructor"].value_counts().reset_index()
    constructor_wins.columns = ["constructor", "wins"]

    # Create pie chart
    fig_constructor_wins = px.pie(
        constructor_wins,
        names="constructor",
        values="wins",
        title="Race Wins by Constructor"
    )

    st.plotly_chart(fig_constructor_wins, use_container_width=True)

    st.divider()

    # Segment distribution
    st.subheader("Race Wins by Drivers")

    # Count wins by drivers
    driver_wins = winner_df["driver_name"].value_counts().reset_index()
    driver_wins.columns = ["driver_name", "driver_wins"]

    fig_driver_wins = px.bar(
        driver_wins,
        x="driver_name",
        y="driver_wins",
        title="Race Wins by Driver"
    )

    st.plotly_chart(fig_driver_wins, use_container_width=True)

    # Total points by driver
    st.subheader("Total Points by Driver")

    driver_points = (df_clean.groupby("driver_name")["points"].sum().reset_index())

    driver_points = driver_points.sort_values(
        by="points",
        ascending=False
    )

    st.dataframe(driver_points, use_container_width=True)

    # Total points by constructor
    st.subheader("Total Points by Constructor")

    constructor_points = (df_clean.groupby("constructor")["points"].sum().reset_index())

    constructor_points = constructor_points.sort_values(
        by="points",
        ascending=False
    )

    st.dataframe(constructor_points, use_container_width=True)

    # Average finishing position by driver
    st.subheader("Average finishing position by Driver")

    driver_point_avg = (df_clean.groupby("driver_name")["points"].mean().reset_index())

    driver_point_avg = driver_point_avg.sort_values(
        by="points",
        ascending=False
    )

    st.dataframe(driver_point_avg, use_container_width=True)


    # Positions gained/lost by race
    st.subheader("Positions Gained/Lost by Race")

    # Create new columns
    df_clean["starting_position"] = df_clean["grid"]
    df_clean["finishing_position"] = df_clean["position"]

    # Calculate gain/loss
    df_clean["loss_or_gain"] = (
        df_clean["starting_position"]
        - df_clean["finishing_position"]
    )

    # Aggregate by race
    loss_or_gain = (
        df_clean.groupby(["race_name", "driver_name"])["loss_or_gain"]
        .sum()
        .reset_index()
    )

    # Sort alphabetically or by gain
    loss_or_gain = loss_or_gain.sort_values(
        by="loss_or_gain",
        ascending=False
    )

    # Display table
    st.dataframe(loss_or_gain, use_container_width=True)
    
    




